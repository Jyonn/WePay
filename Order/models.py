from django.db import models


# class Order(models.Model):
#     """
#     订单类
#     """
#
#     STATUS_CONFIRM_ORDER_BY_SELLER = 5
#     STATUS_CONFIRM_DELIVER = 6
#     STATUS_CONFIRM_RECEIVE = 7
#
#     STATUS_TABLE = (
#         (STATUS_CONFIRM_ORDER_BY_SELLER, '确认接单'),
#         (STATUS_CONFIRM_DELIVER, '确认发货'),
#         (STATUS_CONFIRM_RECEIVE, '确认收货'),
#     )
#
#     L = {
#         'address': 512,
#     }
#
#     buyer = models.ForeignKey(
#         User,
#         verbose_name='买家',
#     )
#     address = models.CharField(
#         verbose_name='买家地址',
#         max_length=L['address'],
#     )
#     good = models.ForeignKey(
#         Good,
#         verbose_name='商品',
#     )
#     price = models.FloatField(
#         verbose_name='购买时单价',
#         default=0,
#     )
#     create_time = models.DateTimeField(
#         verbose_name='创建时间',
#         auto_created=True,
#         auto_now=True,
#     )
#     deliver_time = models.DateTimeField(
#         verbose_name='发货时间',
#         default=None,
#         null=True,
#         blank=True,
#     )
