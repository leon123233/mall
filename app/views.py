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
from weixin.pay import WeixinPay
from weixin.helper import md5_constructor as md5
import xmltodict

logger = logging.getLogger('django')

def build_pay_sign(app_id, nonce_str, prepay_id, time_stamp, key, signType='MD5'):
    """
    :param app_id:
    :param nonce_str:
    :param prepay_id:
    :param time_stamp:
    :param key:
    :param signType:
    :return:
    """
    sign = 'appId={app_id}' \
           '&nonceStr={nonce_str}' \
           '&package=prepay_id={prepay_id}' \
           '&signType={signType}' \
           '&timeStamp={time_stamp}' \
           '&key={key}'.format(app_id=app_id, nonce_str=nonce_str, prepay_id=prepay_id,
                               time_stamp=time_stamp, key=key, signType=signType)
    return md5(sign).hexdigest().upper()

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

def wxapp_pay(request,sub_domain="test"):
    try:
        app =  AppConfig.objects.get(sub_domain="test")
        if not app:
            return HttpResponse(json.dumps({'code': 404, 'msg': error_code[404]}))
        wechat_pay_id = app.wechat_pay_id
        wechat_pay_secret = app.wechat_pay_secret
        if not wechat_pay_id or not wechat_pay_secret:
            return HttpResponse(json.dumps({'code': 404, 'msg': '未设置wechat_pay_id和wechat_pay_secret'}))
        data = request.POST
        token = data["token"]
        money = data["money"]
        remark = data["remark"]
        order_id = data["nextAction"]["id"]
        order = Order.objects.get(id=order_id) 
        access_token = AccessToken.objects.get(token=token)
        user = WechatUser.objects.get(app_id=app,open_id=access_token.open_id)
        payment = Payment(order=order,user=user,price=money,remark=remark)
        payment.save()
        wxpay = WeixinPay(appid=app.app_id, mch_id=wechat_pay_id, partner_key=wechat_pay_secret)
        unified_order = wxpay.unifiedorder(
                body=u'{mall_name}'.format(mall_name=app.name),
                total_fee=int(float(money) * 100),
                notify_url=u'{host}/{sub_domain}/pay/notify'.format(host=app.host, sub_domain="app"),
                openid=u'{}'.format(user.open_id),
                out_trade_no=u'{}'.format(order.order_num)
            )
        if unified_order['return_code'] == 'SUCCESS' and not unified_order['result_code'] == 'FAIL':
            time_stamp = str(int(time.time()))
            data = json.dumps({
                        "code": 0,
                        "data": {
                            'timeStamp': str(int(time.time())),
                            'nonceStr': unified_order['nonce_str'],
                            'prepayId': unified_order['prepay_id'],
                            'sign': build_pay_sign(app_id, unified_order['nonce_str'], unified_order['prepay_id'],
                                                   time_stamp, wechat_pay_secret)
                        },
                        "msg": "success"
                    })
            return HttpResponse(data)
        else:
            if unified_order['err_code'] == 'ORDERPAID':
                payment.status = "pending"
                payment.save()
            return HttpResponse(json.dumps({'code': -1, 'msg': unified_order.get('err_code_des', unified_order['return_msg'])}))

    except Exception,e:
        traceback.print_exc()
        return HttpResponse(json.dumps({'code': -1, 'msg': error_code[-1], 'data': e.message}))

def pay_notify(request,sub_domain="test"):
        try:
            app = AppConfig.objects.get(sub_domain="test")
            if not app:
                data=xmltodict.unparse({
                        'xml': {
                            u'return_code': 'FAIL',
                            u'return_msg': '参数格式校验错误'
                        }
                    })
                return HttpResponse(data)

            xml_data = request.body

            data = xmltodict.parse(xml_data)['xml']
            logger.info(data)
            if data['return_code'] == 'SUCCESS':
                data.update({'status': "success"})
                order = Order.objects.get(order_num=data['out_trade_no'])
                #order.payment_ids.write(data)
                order.status = 1
            else:
                data.update({'status': "failed"})
                order = Order.objects.get(order_num=data['out_trade_no'])

            data=xmltodict.unparse({
                    'xml': {
                        'return_code': u'SUCCESS',
                        'return_msg': u'SUCCESS'
                    }
                })
            return HttpResponse(data)

        except Exception , e:
            traceback.print_exc()

            data=xmltodict.unparse({
                    'xml': {
                        'return_code': u'FAIL',
                        'return_msg': u'服务器内部错误'
                    }
                })
            return HttpResponse(data)
