from dao import BaseDao


class MainDao(BaseDao):
    """获取轮播图"""
    def wheel(self):
        return super(MainDao, self).rand_all("wheel", page_size=4)
    """获取首页分类图标"""
    def main_type(self):
        return super(MainDao, self).search_all("main_type_img")
    """获取首页小图标"""
    def main_small_img(self):
        return super(MainDao, self).search_all("main_small_img", page_size=10)
    """模糊查询商家"""
    def search(self, args):
        sql = "select * from shops where shop_name like '%%%s%%' limit 0,8"
        return super(MainDao, self).query(sql,args)

    """返回优选商家"""
    def youxuan_shops(self):
        return super(MainDao, self).rand_all("shops",page_size=4)
    """精选商品"""
    def youxuan_goods(self):
        return super(MainDao, self).rand_all("goods", page_size=2)

    """到店自取"""
    def shoplists(self):
        return super(MainDao, self).rand_all("shops", page_size=10)

    """附近的商家"""
    def shop_nearby(self,*args):
        sql = "SELECT shops.*, distance(%s, %s, latitude, longitude)  AS dis FROM shops ORDER BY dis ASC "
        return super(MainDao, self).query(sql,*args)

    """获取全部分类"""
    def all_type(self):
        data =  super(MainDao, self).search_all("shop_type")
        for i in data:
            i["list"] = self.all_small(i.get("id"))
        return data

    """获取小分类信息"""
    def all_small(self, id):
        return super(MainDao, self).search_all("shop_small_type" , where = "shop_small_type_shoptype_id" ,args = id)

    """根据店铺id随机选取一张食品图片"""
    def get_goodpic(self,id):
        return super(MainDao, self).rand_all("goods", where='g_shop_id',args=id,page_size=1)[0]['goods_picture']

    """根据店铺id选取店铺名称"""
    def get_shopname(self,id):
        return super(MainDao, self).rand_all("shops", where='id',args=id,page_size=1)[0]['shop_name']

    def get_shop_head_pic(self,id):
        return super(MainDao,self).rand_all("shops",where="id", args=id,page_size=1)[0]['img_url']






