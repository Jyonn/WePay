from django.db import models

from base.error import Error
from base.response import Ret


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
        if not Category.L['category_name'] >= len(name) >= 2:
            return Ret(Error.CATEGORY_NAME_LENGTH)
        o = cls(category_name=name)
        try:
            o.save()
        except:
            return Ret(Error.ERROR_CATEGORY_CREATE)
        return Ret()

    @staticmethod
    def get(category_id):
        """
        根据类别ID获取类别类
        :param category_id: 类别ID
        :return: 类别类
        """
        try:
            o = Category.objects.get(pk=category_id)
        except:
            return Ret(Error.NOT_FOUND_CATEGORY)
        return Ret(Error.OK, o)

    @staticmethod
    def init():
        category_list = ['啤酒', '沐浴露', '洗发水']
        for category in category_list:
            Category.create(category)
        return Ret()

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
        return Ret(Error.OK, category_list)

    @staticmethod
    def get_unset_list(o_user):
        """
        获取用户未设置按钮的类别
        :return: 类别列表
        """
        ret = o_user.get_button_list()
        if ret.error != Error.OK:
            return Ret(ret.error)
        button_list = ret.body
        set_category_list = []
        for button in button_list:
            set_category_list.append(button.category_id)
        unset_category_list = []
        for o_category in Category.objects.all():
            if o_category.pk not in set_category_list:
                unset_category_list.append(dict(
                    category_name=o_category.category_name,
                    category_id=o_category.pk,
                ))
        return Ret(Error.OK, unset_category_list)

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
                pic=o_good.get_pic(),
                description=o_good.description,
                category_name=o_good.category.category_name,
                category_id=o_good.category_id,
            ))
        return Ret(Error.OK, good_list)


class Good(models.Model):
    """
    商品类
    """
    L = {
        'description': 512,
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
    description = models.CharField(
        verbose_name='商品介绍',
        max_length=L['description'],
        default=None,
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
    def create(cls, seller, o_category, name, price, store, pic, description):
        """
        创建商品类
        :param seller: 卖家类
        :param o_category: 商品类别
        :param name: 商品名
        :param price: 商品价格
        :param store: 商品库存
        :param pic: 商品图片
        :param description: 商品描述
        :return: 成功创建返回商品类，失败返回错误原因
        """
        if not Good.L['good_name'] >= len(name) >= 1:  # 商品名长度错误
            return Ret(Error.GOOD_NAME_LENGTH)
        if not Good.L['description'] > len(description):  # 商品描述长度错误
            return Ret(Error.DESCRIPTION_LENGTH)
        try:
            price = float(price)
            assert price > 0
        except:
            return Ret(Error.PRICE)  # 商品价格错误
        try:
            store = int(store)
            assert store > 0
        except:
            return Ret(Error.STORE)  # 商品库存错误
        o = cls(
            category=o_category,
            good_name=name,
            price=price,
            store=store,
            pic=pic,
            seller=seller,
        )
        try:
            o.save()
            return Ret(Error.OK, o)
        except:
            return Ret(Error.ERROR_GOOD_CREATE)

    @staticmethod
    def get(good_id):
        """
        根据商品ID获取商品类
        :param good_id: 商品ID
        :return: 商品类
        """
        try:
            o = Good.objects.get(pk=good_id)
        except:
            return Ret(Error.NOT_FOUND_GOOD)
        return Ret(Error.OK, o)

    def get_info(self):
        """
        获取商品信息
        :return: 商品信息
        """
        good_dict = dict(
            good_name=self.good_name,
            store=self.store,
            price=self.price,
            pic=self.get_pic(),
            description=self.description,
            category_name=self.category.category_name,
        )
        return Ret(Error.OK, good_dict)

    def edit_info(self, seller, name, price, store, description, pic):
        """
        编辑商品属性
        :param seller: 商家用户类
        :param name: 商品名
        :param price: 商品价格
        :param store: 商品库存
        :param description: 商品描述
        :param pic: 商品图片
        :return:
        """
        if self.seller != seller:
            return Ret(Error.NOT_FOUND_GOOD)
        if not Good.L['good_name'] >= len(name) >= 1:  # 商品名长度错误
            return Ret(Error.GOOD_NAME_LENGTH)
        if not Good.L['description'] > len(description):  # 商品描述长度错误
            return Ret(Error.DESCRIPTION_LENGTH)
        try:
            price = float(price)
            assert price > 0
        except:
            return Ret(Error.PRICE)  # 商品价格错误
        try:
            store = int(store)
            assert store > 0
        except:
            return Ret(Error.STORE)  # 商品库存错误

        from base.c_qiniu import QiNiu
        QiNiu.delete(self.pic)

        self.good_name = name
        self.price = price
        self.store = store
        self.description = description
        self.pic = pic
        self.save()

    def lazy_remove(self, o_user):
        """
        删除商品
        """
        if self.seller != o_user:
            return Ret(Error.NOT_FOUND_GOOD)
        self.is_deleted = True
        self.save()
        return Ret()

    def get_pic(self):
        from base.c_qiniu import QiNiu
        return QiNiu.host + self.pic


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
    def create(cls, o_user, o_good, buy_num):
        """
        创建按钮默认购买设置
        :param o_user: 买方
        :param o_good: 默认商品类
        :param buy_num: 默认购买数量
        :return: 创建成功则返回设置类，否则返回错误代码
        """
        try:
            buy_num = int(buy_num)
            assert buy_num > 0
        except:
            return Ret(Error.BUY_NUM)

        if o_good.is_deleted:
            return Ret(Error.DELETED_GOOD)

        from User.models import User
        if o_user.user_type == User.TYPE_SELLER:
            return Ret(Error.REQUIRE_BUYER)

        try:
            Button.objects.get(owner=o_user, category_id=o_good.category_id)
            return Ret(Error.EXIST_BUTTON)
        except:
            pass

        o = cls(
            owner=o_user,
            category=o_good.category,
            default_good=o_good,
            buy_num=buy_num,
        )

        try:
            o.save()
        except:
            return Ret(Error.ERROR_BUTTON_CREATE)
        return Ret(Error.OK, o)

    @staticmethod
    def get(button_id):
        """
        根据按钮ID获取按钮类
        :param button_id: 按钮ID
        :return: 按钮类
        """
        try:
            o = Button.objects.get(pk=button_id)
        except:
            return Ret(Error.NOT_FOUND_BUTTON)
        return Ret(Error.OK, o)

    def edit_info(self, o_user, o_good, buy_num):
        """
        编辑按钮
        :param o_user: 买方用户类
        :param o_good: 商品类
        :param buy_num: 购买数量
        :return: 修改成功失败代码
        """
        if self.owner != o_user:
            return Ret(Error.NOT_YOUR_BUTTON)  # 不是你的按钮
        try:
            buy_num = int(buy_num)
            assert buy_num > 0
        except:
            return Ret(Error.BUY_NUM)  # 错误的购买数量

        if self.category != o_good.category:
            return Ret(Error.NOT_BELONG_CATEGORY)  # 不属于此类别

        self.default_good = o_good
        self.buy_num = buy_num
        self.save()
        return Ret()

    def remove(self, o_user):
        """
        删除按钮
        :param o_user: 买家用户类
        :return: 删除成功失败代码
        """
        if self.owner != o_user:
            return Ret(Error.NOT_YOUR_BUTTON)
        self.delete()
        return Ret()
