# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from models import *
import traceback
import json
import time,datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from .tools import get_wechat_session_info, get_wechat_user_info
from .error_code import error_code
import logging
from .address import AddressManager
from .order import OrderManager

logger = logging.getLogger('django')

# Create your views here.
def  get_config_value(request,subdomain=None):
        try:
            if request.method == 'GET':
                    app =  AppConfig.objects.get(sub_domain="test")
                    key = request.GET.get('key')
                    if not app:
                            return  HttpResponse(json.dumps({'code': 404, 'msg': 'domain not found'}))
                    data = json.dumps({
                        'code': 0,
                        'data': {
                            'creatAt': '2017-01-16 12:09:31',
                            'dateType': 0,
                            'id': 0,
                            'key': key,
                            'remark': '',
                            'updateAt': '2017-01-16 12:09:31',
                            'userId': app.app_id,
                            'value': 'test_value'
                    },
                    'msg': 'success'                          

                        }
                    )        
                    return HttpResponse(data)
        except Exception,e:
                return HttpResponse(json.dumps({'code': 404, 'msg':str(e)}))

def check_token(request, sub_domain=None):
        try:
                if request.method == 'GET':
                    app =  AppConfig.objects.get(sub_domain="test")
                    token = request.GET.get("token")
                    if not token:
                            return  HttpResponse(json.dumps({'code': 300, 'msg': 'missing token'}))
                    access_token =  AccessToken.objects.get(token=token)
                    if not access_token:
                             return  HttpResponse(json.dumps({'code': 901, 'msg': 'wrong token'}))
                    return HttpResponse(json.dumps({'code': 0, 'msg': 'success'}))
        except Exception,e:
                return HttpResponse(json.dumps({'code': 404, 'msg':str(e),'data':''}))

def  login(request,sub_domain=None):
        try:
                if request.method == 'GET':
                        app =  AppConfig.objects.get(sub_domain="test")
                        code = request.GET.get("code")
                        logger.info("code: "+str(code))
                        session_info = get_wechat_session_info(app.app_id, app.secret, code)
                        logger.info(session_info)
                        if session_info.get('errcode'):
                                return HttpResponse(
                                    json.dumps({'code': -1, 'msg': error_code[-1], 'data': session_info.get('errmsg')})
                                )
                        open_id = session_info['openid']
                        user =  WechatUser.objects.filter(open_id=open_id)
                        if not user:
                	    return HttpResponse(json.dumps({'code': 10000, 'msg': error_code[10000]}))
                        user = user[0]
                        access_token = AccessToken.objects.filter(open_id=open_id)
                        session_key = session_info['session_key']
                        token = ''
                        if not access_token:
                            s = Serializer(
                                secret_key=app.secret,
                                salt=app.app_id,
                                expires_in=2 * 3600)
                            timestamp = time.time()
                            token =  s.dumps({'session_key': session_key,'open_id': open_id,'iat': timestamp})
                            a = AccessToken(token=token,open_id=open_id,session_key=session_key)
                            a.save()
                        else:
                            token = access_token[0].token
                        return HttpResponse(json.dumps({'code': 0,'data': {"token":token,"uid":user.id},'msg':"ok"}))
        except Exception,e:
             traceback.print_exc()
             return HttpResponse(json.dumps({'code': -1, 'msg': error_code[-1], 'data': e.message}))

def  register_cplx(request, sub_domain=None):
        try:
                if request.method == 'GET':
                        app =  AppConfig.objects.get(sub_domain="test")
                        code = request.GET.get("code","")
                        encrypted_data = request.GET.get("encryptedData","")
                        iv = request.GET.get("iv","")
                        if not code:
                                return HttpResponse(json.dumps({'code': 300, 'msg': error_code[300].format('code')}))

                        if not encrypted_data:
                                return HttpResponse(json.dumps({'code': 300, 'msg': error_code[300].format('encrypted_data')}))

                        if not iv:
                                return HttpResponse(json.dumps({'code': 300, 'msg': error_code[300].format('iv')}))

                        session_key, user_info = get_wechat_user_info(app.app_id, app.secret, code, encrypted_data, iv)
                        user = WechatUser(
                            app_id = app,
                            name=user_info['nickName'],
                            open_id=user_info['openId'],
                            gender=user_info['gender'],
                            language=user_info['language'],
                            #country=user_info['country'],
                            province=user_info['province'],
                            city=user_info['city'],
                            last_login = datetime.datetime.now()
                            )
                        user.save()
                        return HttpResponse(json.dumps({'code': 0, 'msg': 'success'}))
        except Exception,e:
                traceback.print_exc()
                return HttpResponse(json.dumps({'code': -1, 'msg': error_code[-1], 'data': e.message}))

def  banner_list(request,sub_domain=None, default_banner=True):
        try:
                if request.method == 'GET':
                    app =  AppConfig.objects.get(sub_domain="test")
                    banner_list =  Banner.objects.filter(sub_domain="test")
                    if banner_list:
                            data = [{
                            "businessId": each_banner.goods.id,
                            "dateAdd": "2017-01-16 12:09:31",
                            "dateUpdate": "2017-01-16 12:09:31",
                            "id": each_banner.id,
                            "linkUrl": '',
                            "paixu": 0,
                            "picUrl": each_banner.display_pic,
                            "remark": each_banner.remark,
                            "status": 0,
                            "statusStr": u"显示",
                            "title": each_banner.title,
                            "type": "0",
                            "userId": app.id,
                            } for each_banner in banner_list                           
                        ]
                    data=json.dumps({
                    "code": 0,
                    "data": data,
                    "msg": "success"
                    })
                    return HttpResponse(data)
        except Exception,e:
                traceback.print_exc()
                return HttpResponse(json.dumps({'code': -1, 'msg': error_code[-1], 'data': e.message}))

def all_category(request,sub_domain=None):
    try:
	if request.method == "GET":
           app =  AppConfig.objects.get(sub_domain="test")
           all_category = Category.objects.filter(sub_domain="test")
           data=json.dumps(
                    {
                        "code": 0,
                        "data": [
                            {
                                "dateAdd": "",
                                "dateUpdate": "",
                                "icon": each_category.icon,
                                "id": each_category.id,
                                "isUse": True,
                                "key": each_category.key,
                                "level": 1,
                                "name": each_category.name,
                                "paixu": 0,
                                "pid": 0,
                                "type": each_category.c_type,
                                "userId": app.id
                            } for each_category in all_category
                        ],
                        "msg": "success"
                    })
	   return HttpResponse(data)
    except Exception,e:
       traceback.print_exc()
       return HttpResponse(json.dumps({'code': -1, 'msg': error_code[-1], 'data': e.message}))

           
		    

def goods_list(request,sub_domain=None):
    try:
	if request.method == "GET":
           app =  AppConfig.objects.get(sub_domain="test")
           category_id = request.GET.get("categoryId",None)
           if category_id:
               category = Category.objects.get(id=category_id)
               goods = Goods.objects.filter(app_id=app,category=category)
           else:
               goods = Goods.objects.filter(app_id=app)
           data=json.dumps({
                    "code": 0,
                    "data": [
                        {
                            "categoryId": each_goods.category.id,
                            "characteristic": each_goods.characteristic,
                            "dateAdd": "2017-01-16 12:09:31",
                            "dateUpdate": "2017-01-16 12:09:31",
                            "id": each_goods.id,
                            "logisticsId": 0,
                            "minPrice": each_goods.min_price,
                            "name": each_goods.name,
                            "numberFav": 0,
                            "numberGoodReputation": each_goods.number_good_reputation,
                            "numberOrders": each_goods.number_order,
                            "originalPrice": each_goods.original_price,
                            "paixu": 0,
                            "pic": each_goods.display_pic,
                            "recommendStatus": 0,
                            "recommendStatusStr": "",
                            "shopId": 0,
                            "status": 0,
                            "statusStr": u"上架",
                            "stores": each_goods.stores,
                            "userId": app.id,
                            "views": 0,
                            "weight": 0
                        } for each_goods in goods
                    ],
                    "msg": "success"
                })           
           
	   return HttpResponse(data)
    except Exception,e:
       traceback.print_exc()
       return HttpResponse(json.dumps({'code': -1, 'msg': error_code[-1], 'data': e.message}))

def goods_detail(request,sub_domain=None):
    try:
	if request.method == "GET":
           app =  AppConfig.objects.get(sub_domain="test")
           goods_id = request.GET.get("id",None)
           goods = Goods.objects.get(id=goods_id)
           data = {
                "code": 0,
                "data": {
                    "category": {
                        "dateAdd": "2017-01-16 12:09:31",
                        "dateUpdate": "2017-01-16 12:09:31",
                        "icon": goods.category.icon,
                        "id": goods.category.id,
                        "isUse": True,
                        "key": goods.category.key,
                        "name": goods.category.name,
                        "paixu": 0,
                        "pid": 0,
                        "type": goods.category.c_type,
                        "userId": app.id
                    },
                    "pics": [
                        {
                            "goodsId": goods.id,
                            "id": each_pic.id,
                            "pic": app.host+"/media/"+str(each_pic.pic)
                        } for each_pic in goods.pics.all()
                    ],
                    "logistics": {
                        "logisticsBySelf": 0,
                        "isFree": True,
                        "by_self": 0,
                        "feeType": 0,
                        "feeTypeStr": "",
                        "details": []
                    },
                    "content": "<p>%s</p>" % goods.content,
                    "basicInfo": {
                        "categoryId": goods.category.id,
                        "characteristic": goods.characteristic or '',
                        "dateAdd": "2017-01-16 12:09:31",
                        "dateUpdate": "2017-01-16 12:09:31",
                        "id": goods.id,
                        "logisticsId": 0,
                        "minPrice": goods.min_price,
                        "name": goods.name,
                        "numberFav": 0,
                        "numberGoodReputation": goods.number_good_reputation,
                        "numberOrders": goods.number_order,
                        "originalPrice": goods.original_price,
                        "paixu": 0,
                        "pic": goods.display_pic,
                        "recommendStatus": 0,
                        "recommendStatusStr": "",
                        "shopId": 0,
                        "status": 0,
                        "statusStr": u"上架",
                        "stores": goods.stores,
                        "userId": app.id,
                        "views": 0,
                        "weight": goods.weight
                    }
                },
                "msg": "success"
            }
           
	   return HttpResponse(json.dumps(data))
    except Exception,e:
       traceback.print_exc()
       return HttpResponse(json.dumps({'code': -1, 'msg': error_code[-1], 'data': e.message}))


def address_list(request,sub_domain="test"):
    a = AddressManager(request,sub_domain)
    return a.address_list()
def address_add(request,sub_domain="test"):
    return AddressManager(request,sub_domain).address_add()
def address_update(request,sub_domain="test"):
    return AddressManager(request,sub_domain).address_update()
def address_detail(request,sub_domain="test"):
    return AddressManager(request,sub_domain).address_detail()
def address_delete(request,sub_domain="test"):
    return AddressManager(request,sub_domain).address_delete()
def address_default(request,sub_domain="test"):
    return AddressManager(request,sub_domain).address_default()


def order_list(request,sub_domain="test"):
    return OrderManager(request,sub_domain).order_list()
def order_create(request,sub_domain="test"):
    return OrderManager(request,sub_domain).order_create()
def order_detail(request,sub_domain="test"):
    return OrderManager(request,sub_domain).order_detail()
def order_close(request,sub_domain="test"):
    return OrderManager(request,sub_domain).order_close()
def order_statistics(request,sub_domain="test"):
    return OrderManager(request,sub_domain).order_statistics()

    
