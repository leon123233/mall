# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponseRedirect, HttpResponse
from models import *
import traceback
import json
import time,datetime
from .tools import get_wechat_session_info, get_wechat_user_info
from .error_code import error_code
import logging
logger = logging.getLogger('django')

def try_catch(func):
    def _wrap(*args):
        try:
            r = func(*args)
            return r
        except Exception,e:
            traceback.print_exc()
            return HttpResponse(json.dumps({'code': -1, 'msg': error_code[-1], 'data': e.message})) 
    return _wrap

class OrderManager(object):
    
    def __init__(self,request,sub_domain):
        self.app = AppConfig.objects.get(sub_domain=sub_domain)
        self.request = request
        if request.method == "GET":
            token = request.GET.get("token")
        elif request.method == "POST":
            token = request.POST.get("token")
        else:
            token = ""
        accesstoken = AccessToken.objects.get(token=token)
        self.user = WechatUser.objects.get(open_id=accesstoken.open_id)

    @try_catch
    def order_list(self):
        status = self.request.GET.get("status")
        if not status:
            orders = Order.objects.filter(user=self.user)
        else:
            orders = Order.objects.filter(user=self.user,status=status)
        data=json.dumps({
                    "code": 0,
                    "data": {
                        "orderList": [{
                            "amountReal": each_order.total,
                            "dateAdd": each_order.date.strftime('%Y-%m-%d %H:%M:%S'),
                            "id": each_order.id,
                            "orderNumber": each_order.order_num,
                            "status": each_order.status,
                            "statusStr": "",
                            "remark":each_order.remark,
                            
                        } for each_order in orders],
                        "goodsMap": {
                            each_order.id: [
                                {
                                    "pic": self.app.host+"/media/"+str(each_goods.display_pic),
                                } for each_goods in each_order.goods.all()]
                            for each_order in orders}
                    },
                    "msg": "success"
                })
        return HttpResponse(data)

    def _handle_goods_json(self, goods_json):
        """
        :param goods_json: dict
        :param province_id: 省
        :param city_id: 市
        :param district_id: 区
        :return:goods_price, logistics_price, total, goods_list
        """
        goods_price = 0.0

        for each_goods in goods_json:
            amount = each_goods['number']
            goods = Goods.objects.get(id=each_goods["goodsId"])
            each_goods_total = amount * goods.min_price 
            goods_price += each_goods_total
        return goods_price

    @try_catch
    def order_create(self):
        data=self.request.POST
        goods_json = json.loads(data.get('goodsJsonStr'))
        province_id = data.get('provinceId')
        city_id = data.get('cityId')
        remark = data.get('remark')
        address = data.get("address")
        phone = data.get("mobile")
        link_man = data.get("linkMan")

        goods_price = self._handle_goods_json(goods_json)
        
        try:
            discount = Discount.objects.get(app=self.app,status=1)
            if goods_price >= discount.man:
                goods_price = goods_price - discount.jian                
        except:
            pass

        order_dict = {
                'user': self.user,
                'number_goods': len(goods_json),
                'goods_price': goods_price,
                'total': goods_price,
                'province_id': province_id,
                'city_id': city_id,
                #'district_id': district_id,
                'link_man':link_man,
                'phone':phone,
                'address':address,
                'status':0,
                'remark':remark,
                'logistics_price':0.0,
                'date':datetime.datetime.now(),
                'order_num':"OD"+str(int(time.time())),
            }
        order = Order(**order_dict)
        order.save()
        for goods_dict in goods_json:
            goods_id = goods_dict['goodsId']
            g = Goods.objects.get(id=goods_id)
            o = OrderGoods(order=order,goods=g,amount=goods_dict["number"])
            o.save()
            order.goods.add(g)
        order.save()
        
        return HttpResponse(json.dumps({'code': 0, 'msg': 'success'}))

    @try_catch
    def order_close(self):
        order_id=self.request.GET.get("orderId")
        order = Order.objects.get(id=order_id)
        order.status = -1
        order.save()
        return HttpResponse(json.dumps({'code': 0, 'msg': 'success'}))
 
    @try_catch
    def order_statistics(self):
        orders = Order.objects.filter(user=self.user)
	data = {
  	"code": 0,
  	"data": {
        "count_id_close":len(orders.filter(status=-1)),
        "count_id_no_transfer":0,
    	"count_id_no_pay": len(orders.filter(status=0)),
    	"count_id_no_confirm": len(orders.filter(status=2)),
    	"count_id_success": len(orders.filter(status__gt=2))
  	},
  	"msg": "success"
	}        
        return HttpResponse(json.dumps(data))

    @try_catch
    def order_detail(self):
        order_id = self.request.GET.get("id")
        order = Order.objects.get(id=order_id)
        data = {
                "code": 0,
                "data": {
                    "orderInfo": {
                        "amount": order.goods_price,
                        "amountLogistics": 0,
                        "amountReal": order.total,
                        "dateAdd": order.date,
                        "dateUpdate": order.date,
                        "goodsNumber": order.number_goods,
                        "id": order.id,
                        "orderNumber": order.order_num,
                        "remark": order.remark,
                        "status": order.status,
                        "statusStr": "",
                        "type": 0,
                        "uid": self.app.id,
                        "userId": self.user.id
                    },
                    "goods": [
                        {
                            "amount": each.goods.min_price,
                            "goodsId": each.goods.goods_id,
                            "goodsName": each.goods.name,
                            "id": each.goods.id,
                            "number": each.amount,
                            "orderId": order.id,
                            "pic": each.goods.display_pic,
                            "property": ""
                        } for each in order.goods_amount
                    ],
                    "logistics": {
                        "address": order.address.address,
                        "cityId": order.address.city_id,
                        "code": "",
                        "dateUpdate": order.date,
                        "districtId": "",
                        "linkMan": order.address.linkman,
                        "mobile": order.address.phone,
                        "provinceId": order.address.province_id,
                        "shipperCode": '',
                        "shipperName": '',
                        "status": 1,
                        "trackingNumber":''
                    },
                },
                "msg": "success"
            }
        return HttpResponse(json.dumps(data))
