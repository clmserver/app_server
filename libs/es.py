"""
封装ElasticSearch搜索引擎的SDK(library库)
"""
import requests
import pymysql
from pymysql.cursors import DictCursor


class ESearch():
    def __init__(self, index):
        self.host = '121.199.63.71'
        self.port = '9202'
        self.index = index

    def create_index(self):
        url = f'http://{self.host}:{self.port}/{self.index}'
        resp = requests.put(url, json={
            "settings": {
                "number_of_shards": 5,
                "number_of_replicas": 1
            }
        })
        resp_data = resp.json()
        # print(resp_data)
        if resp_data.get('acknowledged'):
            print('create %s index %s ok!' % (self.port, self.index))

    def remove_index(self):
        url = f'http://{self.host}:{self.port}/{self.index}'
        requests.delete(url)

    def add_doc(self, doc_type, id=None, **values):
        url = f'http://{self.host}:{self.port}/{self.index}/{doc_type}/'
        if id:
            url += f"{id}"
        resp = requests.post(url, json=values)
        resp_data = resp.json()
        # print(resp_data)
        if resp_data.get('result') == "created":
            print('add doc %s ok!' % values)
        else:
            print('add doc %s error!' % values)

    def query(self, keyword):
        url = f'http://{self.host}:{self.port}/{self.index}/_search?q={keyword}'
        resp = requests.get(url)
        resp_data = resp.json()
        # print(resp_data,'xxxxxxxxxx')
        if resp_data.get('hits').get('total') > 0:
            return {
                'code': 200,
                'total': resp_data.get('hits').get('total'),
                'datas': [data.get('_source')
                          for data in resp_data.get('hits').get('hits')
                          ]
            }
        else:
            return {'code': 201, 'msg': '无'}


def init_index():
    db = pymysql.Connect(host="localhost",
                         port=3306,
                         user='mtadmin',
                         password='mt9900',
                         db='mt_api_db',
                         charset='utf8')
    # db = pymysql.Connect(host="10.35.162.134",
    #                      port=3306,
    #                      user='root',
    #                      password='710043',
    #                      db='navmore',
    #                      charset='utf8')
    with db.cursor(cursor=DictCursor) as c:
        c.execute('select * from shops')
        es_ = ESearch('mtindex')
        es_.create_index()
        for row_data in c.fetchall():
            # print(row_data)
            es_.add_doc('shop', **row_data)

        print('__init add shop doc_type all ok--')


if __name__ == '__main__':
    # init_index()
    search = ESearch('mtindex')
    # search.remove_index()
    print(search.query('王'))
