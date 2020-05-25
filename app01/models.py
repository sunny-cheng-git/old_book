from django.db import models
from old_books import settings

from django.contrib.auth.models import AbstractUser
class UserInfo(AbstractUser):
    """
    用户信息
    """
    nid = models.AutoField(primary_key=True)
    balance = models.IntegerField(verbose_name='用户余额',null=True)

class Category(models.Model):
    cid = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name="文章分类",max_length=32,null=True)


class Book(models.Model):
    sid = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name="书名",max_length=32)
    img = models.FileField(upload_to='book_imgs/', default="/book_imgs/default.jpg")
    price = models.FloatField(verbose_name="价格")
    author = models.CharField(verbose_name="作者",max_length=32,null=True)
    publish = models.CharField(verbose_name="出版社",max_length=32,null=True)
    pub_time = models.DateField(verbose_name="出版时间",null=True)
    brief = models.CharField(verbose_name="简介",max_length=200)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    category = models.ManyToManyField(to='Category')

class Book_detail(models.Model):
    sell_book = models.OneToOneField(Book,on_delete=models.CASCADE)
    status_choices = ((0, '正常销售'), (1, '已售罄'), (2, '已下架'), (3, '暂时无货'))
    status = models.SmallIntegerField(choices=status_choices, verbose_name="状态",default=0)
    book_count = models.IntegerField(verbose_name='在售书籍数量',null=True,default=1) #这里默认应该是一本



class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    payment_number = models.CharField(max_length=128, verbose_name="支付第3方订单号", null=True, blank=True)
    order_number = models.CharField(max_length=128, verbose_name="订单号", unique=True)  # 考虑到订单合并支付的问题
    actual_amount = models.FloatField(verbose_name="实付金额")
    status_choices = ((0, '交易成功'), (1, '待支付'), (2, '退费申请中'), (3, '已退费'), (4, '主动取消'), (5, '超时取消'))
    status = models.SmallIntegerField(choices=status_choices, verbose_name="状态")
    date = models.DateTimeField(auto_now_add=True, verbose_name="订单生成时间")
    pay_time = models.DateTimeField(blank=True, null=True, verbose_name="付款时间")
    cancel_time = models.DateTimeField(blank=True, null=True, verbose_name="订单取消时间")


class OrderDetail(models.Model):
    """订单详情"""
    order = models.ForeignKey("Order", on_delete=None)
    book = models.ForeignKey(Book, on_delete=None)
    original_price = models.FloatField("书籍原价")
    price = models.FloatField("折后价格")
    memo = models.CharField(max_length=255, blank=True, null=True, verbose_name="备忘录")

# 点赞评论表
class Comment(models.Model):
    cid = models.AutoField(primary_key=True)
    content = models.CharField(verbose_name="评论", max_length=200)
    book =models.ForeignKey(verbose_name='评论书籍',to='Book',to_field='sid',on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,verbose_name='评论者',on_delete=models.CASCADE)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    parent_comment = models.ForeignKey('self', null=True, on_delete=models.CASCADE)
    up_count = models.IntegerField(default=0)
    score = models.SmallIntegerField(null=True)


class Book_up_down(models.Model):
    bid = models.AutoField(primary_key=True)
    comment =models.ForeignKey(verbose_name='点赞评论',to='Comment',to_field='cid',on_delete=models.CASCADE,default=None)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    is_up = models.BooleanField(default=True)


class Shopping_car(models.Model):
    sid = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=None)
    book = models.ForeignKey(Book,on_delete=None)