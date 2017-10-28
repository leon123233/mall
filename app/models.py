# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class AppConfig(models.Model):
        sub_domain =  models.CharField(max_length=255)
        host = models.CharField(max_length=255)
        mall_name =  models.CharField(max_length=255)
        app_id =  models.CharField(max_length=255)
        secret =  models.CharField(max_length=255)
        webchat_pay_id =  models.CharField(max_length=255)
        wechat_pay_secret = models.CharField(max_length=255)
class AccessToken(models.Model):
        session_key =  models.CharField(max_length=255)
        open_id =  models.CharField(max_length=255)
        token =  models.CharField(max_length=255)

class WechatUser(models.Model):
        app_id =  models.ForeignKey(AppConfig, on_delete=models.CASCADE)
        name =  models.CharField(max_length=255)
        open_id =  models.CharField(max_length=255)
        gender =  models.CharField(max_length=255)
        language =  models.CharField(max_length=255)
        province = models.CharField(max_length=255)
        city = models.CharField(max_length=255)
        register_type =  models.CharField(max_length=255)
        register_ip =  models.CharField(max_length=255)
        last_login =  models.DateField()
        phone =  models.CharField(max_length=255)
        union_id =  models.CharField(max_length=255)
        ip =  models.CharField(max_length=255)
        status =  models.CharField(max_length=255,default='default')
               
class Category(models.Model):
        sub_domain = models.CharField(max_length=255,help_text="子域名")
	key = models.CharField(max_length=255)
        name =  models.CharField(max_length=255)
        c_type = models.CharField(max_length=255)
        icon = models.CharField(max_length=255)

class Goods(models.Model):
        name =  models.CharField(max_length=255)
        characteristic =  models.CharField(max_length=255)
        #webchat_pay_id =  models.CharField(max_length=255)
        app_id =  models.ForeignKey(AppConfig, on_delete=models.CASCADE)
        category =  models.ForeignKey(Category)
        display_pic =  models.CharField(max_length=255)
        #pic = models.ManyToManyField(Picture)
        content =  models.CharField(max_length=255)
        number_order = models.IntegerField()
        #price_ids =  models.CharField(max_length=255)
        original_price =  models.FloatField()
        min_price =  models.FloatField()
        number_good_reputation =  models.IntegerField(default=0)
        weight =  models.FloatField()
        stores = models.IntegerField()


class Picture(models.Model):
        name =  models.CharField(max_length=255)
        pic = models.ImageField(upload_to='img')
        goods = models.ForeignKey(Goods, related_name="pics",on_delete=models.CASCADE)

class Address(models.Model):
        user = models.ForeignKey(WechatUser, related_name="addr",on_delete=models.CASCADE)
        phone = models.CharField(max_length=255)
        address = models.CharField(max_length=1024)
        link_man = models.CharField(max_length=255)
        status = models.CharField(max_length=255)
        date_update = models.DateField()
        is_default = models.BooleanField()
        province = models.CharField(max_length=255)
        province_id = models.IntegerField()
        city = models.CharField(max_length=255)
        city_id = models.IntegerField()
        area = models.CharField(max_length=255)

class Banner(models.Model):
        sub_domain =  models.CharField(max_length=255)
        title = models.CharField(max_length=255)
        display_pic = models.CharField(max_length=255)
        link_url = models.CharField(max_length=255)
        goods = models.ForeignKey(Goods)
        remark = models.CharField(max_length=255)
        status = models.CharField(max_length=255)


class Order(models.Model):
        user = models.ForeignKey(WechatUser, on_delete=models.CASCADE)
        order_num = models.CharField(max_length=255)
        goods = models.ManyToManyField(Goods)
        address = models.CharField(max_length=1024)
        number_goods = models.IntegerField()
        goods_price = models.FloatField()
        logistics_price = models.FloatField()
        total = models.FloatField()
        status = models.IntegerField()
        tracking_number = models.CharField(max_length=255)
        date = models.DateTimeField()
        remark = models.CharField(max_length=1024)
        link_man = models.CharField(max_length=255)
        province_id = models.IntegerField()
        city_id = models.IntegerField()
        phone = models.CharField(max_length=255)
        #payments
 
class OrderGoods(models.Model):
        order = models.ForeignKey(Order,related_name="goods_amount")
        goods = models.ForeignKey(Goods)
        amount = models.IntegerField()

class Payment(models.Model):
        #dan wei   fen
        order = models.ForeignKey(Order, related_name="pays",on_delete=models.CASCADE)
        #payment_number = models.AutoField()
        user = models.ForeignKey(WechatUser)
        status = models.CharField(max_length=255)
        remark = models.CharField(max_length=255)
        openid = models.CharField(max_length=255)
        price = models.FloatField()
        result_code = models.CharField(max_length=255)
        err_code = models.CharField(max_length=255)
        err_code_des = models.CharField(max_length=255)
        transaction_id = models.CharField(max_length=255)
        bank_type = models.CharField(max_length=255)
        fee_type = models.CharField(max_length=255)
        total_fee = models.IntegerField()
        settlement_total_fee = models.IntegerField()
        cash_fee = models.IntegerField()
        cash_fee_type = models.CharField(max_length=255)
        coupon_fee = models.IntegerField()
        coupon_count = models.IntegerField()




