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
                name=o_category.category_name,
                category_id=o_category.pk,
            ))
        return category_list


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

    def edit_info(self, name, price, store):
        """
        编辑商品属性
        :param name: 商品名
        :param price: 商品价格
        :param store: 商品库存
        :return:
        """
        self.good_name = name
        self.price = price
        self.store = store
        self.save()

    def change_pic(self, pic):
        """
        更换商品图片
        :param pic: 商品图片
        """
        self.pic = pic
        self.save()

    def lazy_remove(self):
        """
        删除商品
        """
        self.is_deleted = True
        self.save()
