# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from models import *
import traceback
import json
import time
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from .tools import get_wechat_session_info, get_wechat_user_info
from .error_code import error_code
import logging

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
                        user =  WechatUser.objects.get(open_id=open_id)
                        access_token = AccessToken.objects.get(open_id=open_id)
                        session_key = session_info['session_key']
                        token = ''
                        if not access_token:
                            s = Serializer(
                                secret_key=app.secret_key,
                                salt=app.app_id,
                                expires_in=2 * 3600)
                            timestamp = time.time()
                            token =  s.dumps({'session_key': session_key,'open_id': open_id,'iat': timestamp})
                            a = AccessToken(token=token,open_id=open_id,session_key=session_key)
                            a.save()
                        return HttpResponse(json.dumps({'code': 0,'token': token}))
        except Exception,e:
             traceback.print_exc()
             return HttpResponse(json.dumps({'code': -1, 'msg': error_code[-1], 'data': e.message}))

def  register_cplx(request, sub_domain=None):
        try:
                if request.method == 'GET':
                        app =  AppConfig.objects.get(sub_domain="test")
                        code = request.GET.get("code","")
                        encrypted_data = request.GET.get("encrypted_data","")
                        iv = request.GET.get("iv","")
                        if not code:
                                return HttpResponse(json.dumps({'code': 300, 'msg': error_code[300].format('code')}))

                        if not encrypted_data:
                                return HttpResponse(json.dumps({'code': 300, 'msg': error_code[300].format('encrypted_data')}))

                        if not iv:
                                return HttpResponse(json.dumps({'code': 300, 'msg': error_code[300].format('iv')}))

                        session_key, user_info = get_wechat_user_info(app_id, secret, code, encrypted_data, iv)
                        user = WechatUser(
                            name=user_info['nickName'],
                            open_id=user_info['openId'],
                            gender=user_info['gender'],
                            language=user_info['language'],
                            country=user_info['country'],
                            province=user_info['province'],
                            city=user_info['city'],
                            )
                        return HttpResponse(json.dumps({'code': 0, 'msg': 'success'}))
        except Exception,e:
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
                return HttpResponse(json.dumps({'code': -1, 'msg': error_code[-1], 'data': e.message}))

