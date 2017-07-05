from django.db import models


# class Good(models.Model):
#     """
#     商品类
#     """
#     L = {
#         'good_name': 20,
#     }
#     good_name = models.CharField(
#         verbose_name='商品名称',
#         max_length=L['good_name'],
#     )
#     price = models.FloatField(
#         verbose_name='单价',
#         default=0,
#     )
#     store = models.IntegerField(
#         verbose_name='余量',
#         default=0,
#     )
#     seller = models.ForeignKey(
#         User,
#         verbose_name='所属卖家',
#     )
#     is_deleted = models.BooleanField(
#         verbose_name='是否删除',
#         default=False,
#     )
