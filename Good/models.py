from django.db import models

from base.error import Error
from base.response import ret


class Category(models.Model):
    """
    商品类别类
    """
    L = {
        'category_name': 20,
    }
    category_name = models.CharField(
        verbose_name='商品类别',
        max_length=L['category_name'],
        unique=True,
    )

    @classmethod
    def create(cls, name):
        """
        创建商品类别
        :param name: 类别名称
        """
        o = cls(category_name=name)
        try:
            o.save()
        except:
            pass

    @staticmethod
    def init():
        category_list = ['啤酒', '沐浴露', '洗发水']
        for category in category_list:
            Category.create(category)

    @staticmethod
    def get_list():
        """
        获取类别列表
        :return: 类别列表
        """
        category_list = []
        for o_category in Category.objects.all():
            category_list.append(dict(
                category_name=o_category.category_name,
                category_id=o_category.pk,
            ))
        return ret(Error.OK, category_list)

    def get_good_list(self):
        """
        获取一个类别的所有商品
        :return: 商品列表
        """
        goods = Good.objects.filter(category=self, is_deleted=False)
        good_list = []
        for o_good in goods:
            good_list.append(dict(
                good_id=o_good.pk,
                brand=o_good.seller.brand,
                good_name=o_good.good_name,
                store=o_good.store,
                price=o_good.price,
                pic=o_good.pic,
            ))
        return ret(Error.OK, good_list)


class Good(models.Model):
    """
    商品类
    """
    L = {
        'good_name': 20,
        'pic': 128,
    }
    category = models.ForeignKey(
        Category,
        verbose_name='所属商品类别',
    )
    good_name = models.CharField(
        verbose_name='商品名称',
        max_length=L['good_name'],
    )
    price = models.FloatField(
        verbose_name='商品单价',
        default=0,
    )
    store = models.IntegerField(
        verbose_name='库存',
        default=0,
    )
    pic = models.CharField(
        verbose_name='商品图片',
        max_length=L['pic'],
    )
    seller = models.ForeignKey(
        'User.User',
        verbose_name='所属卖家',
    )
    is_deleted = models.BooleanField(
        verbose_name='是否删除',
        default=False,
    )

    @classmethod
    def create(cls, seller, category_id, name, price, store, pic):
        """
        创建商品类
        :param seller: 卖家类
        :param category_id: 商品类别ID
        :param name: 商品名
        :param price: 商品价格
        :param store: 商品库存
        :param pic: 商品图片
        :return: 成功创建返回商品类，失败返回错误原因
        """
        o = cls(
            category_id=category_id,
            good_name=name,
            price=price,
            store=store,
            pic=pic,
            seller=seller,
        )
        try:
            o.save()
            return ret(Error.OK, o)
        except:
            return ret(Error.ERROR_GOOD_CREATE)

    # def edit_info(self, name, price, store):
    #     """
    #     编辑商品属性
    #     :param name: 商品名
    #     :param price: 商品价格
    #     :param store: 商品库存
    #     :return:
    #     """
    #     self.good_name = name
    #     self.price = price
    #     self.store = store
    #     self.save()
    #
    # def change_pic(self, pic):
    #     """
    #     更换商品图片
    #     :param pic: 商品图片
    #     """
    #     self.pic = pic
    #     self.save()

    def lazy_remove(self, o_user):
        """
        删除商品
        """
        if self.seller != o_user:
            return ret(Error.NOT_FOUND_GOOD)
        self.is_deleted = True
        self.save()
        return ret()


class Button(models.Model):
    owner = models.ForeignKey(
        'User.User',
        verbose_name='关联用户',
    )
    category = models.ForeignKey(
        'Good.Category',
        verbose_name='关联商品类别',
    )
    default_good = models.ForeignKey(
        'Good.Good',
        verbose_name='默认购买商品'
    )
    buy_num = models.IntegerField(
        verbose_name='默认购买数量',
    )

    @classmethod
    def create(cls, o_user, good_id, buy_num):
        """
        创建按钮默认购买设置
        :param o_user: 买方
        :param good_id: 默认商品ID
        :param buy_num: 默认购买数量
        :return: 创建成功则返回设置类，否则返回错误代码
        """
        try:
            buy_num = int(buy_num)
            assert buy_num > 0
        except:
            return ret(Error.BUY_NUM)
        try:
            o_good = Good.objects.get(pk=good_id)
            if o_good.is_deleted:
                return ret(Error.DELETED_GOOD)
        except:
            return ret(Error.NOT_FOUND_GOOD)

        from User.models import User
        if o_user.user_type == User.TYPE_SELLER:
            return ret(Error.REQUIRE_BUYER)

        try:
            o = Button.objects.get(owner=o_user, category_id=o_good.category_id)
        except:
            o = cls(
                owner=o_user,
                category_id=o_good.category_id,
                good_id=good_id,
                buy_num=buy_num,
            )
            try:
                o.save()
                return ret(Error.OK, o)
            except:
                return ret(Error.ERROR_BUTTON_CREATE)
        o.default_good = o_good
        o.buy_num = buy_num
        o.save()
        return ret(Error.OK, o)
