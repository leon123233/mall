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

def try_catch(func):
    def _wrap(*args):
        try:
            r = func(*args)
            return r
        except Exception,e:
            traceback.print_exc()
            return HttpResponse(json.dumps({'code': -1, 'msg': error_code[-1], 'data': e.message})) 
    

class AddressManager(object):
    
    def AddressManager(self,request,sub_domain):
        self.app = AppConfig.objects.get(sub_domain=sub_domain)
        self.request = request
        token = request.GET.get("token")
        accesstoken = AccessToken.objects.get(token=token)
        self.user = WechatUser.objects.get(open_id=accesstoken.open_id)

    @try_catch
    def address_list(self):
        data=json.dumps({
                    "code": 0,
                    "data": [{
                        "address": each_address.address,
                        "areaStr": each_address.area or '',
                        "cityId": each_address.city_id,
                        "cityStr": each_address.city,
                        "code": "",
                        "dateAdd": each_address.date_update.strftime('%Y-%m-%d %H:%M:%S'),
                        "dateUpdate": each_address.date_update.strftime('%Y-%m-%d %H:%M:%S'),
                        "districtId": 0,
                        "id": each_address.id,
                        "isDefault": each_address.is_default,
                        "linkMan": "",
                        "mobile": each_address.phone,
                        "provinceId": each_address.province_id,
                        "provinceStr": each_address.province,
                        "status": 0,
                        "statusStr": "",
                        "uid": self.app.id,
                        "userId": self.user.id
                    } for each_address in self.user.addr.all()],
                    "msg": "success"
                })
        return HttpResponse(data)
        
    @try_catch
    def address_add(self):
        data=json.loads(self.request.raw_post_data)
        addr = Address(user=self.user,address=data["address"],is_default=data["isDefault"],
                 link_man = data["linkMan"],phone=data["mobile"],date_update=datetime.datetime.now(),
                 city_id = data["cityId"],province_id=data["provinceId"])
        addr.save()       
        return HttpResponse({'code': 0, 'msg': 'success'})
    
    @try_catch
    def address_update(self):
        data=json.loads(self.request.raw_post_data)
        addr = Address.objects.get(id=data["id"])
        addr.address = data["address"]
        addr.is_default = data["isDefault"]
        addr.link_man = data["linkMan"]
        addr.phone = data["mobile"]
        addr.city_id = data["cityId"]
        addr.province_id = data["provinceId"]
        addr.save()
        return HttpResponse({'code': 0, 'msg': 'success'})

    @try_catch
    def address_delete(self):
        addr = Address.objects.get(id=self.request.GET.get("id"))
        addr.delete()
        return HttpResponse({'code': 0, 'msg': 'success'})
    @try_catch
    def address_default(self):
        addr = Address.objects.get(is_default=True,user=self.user)
        
        data=json.dumps({
                    "code": 0,
                    "data": {
                        "address": addr.address,
                        "areaStr": addr.area or '',
                        "cityId": addr.city_id,
                        "cityStr": each_address.city,
                        "code": "",
                        "dateAdd": addr.date_update.strftime('%Y-%m-%d %H:%M:%S'),
                        "dateUpdate": addr.date_update.strftime('%Y-%m-%d %H:%M:%S'),
                        "districtId": 0,
                        "id": addr.id,
                        "isDefault": addr.is_default,
                        "linkMan": "",
                        "mobile": addr.phone,
                        "provinceId": addr.province_id,
                        "provinceStr": addr.province,
                        "status": 0,
                        "statusStr": "",
                        "uid": self.app.id,
                        "userId": self.user.id
                    },
                    "msg": "success"
                })
        return HttpResponse(data)
    
    @try_catch
    def address_detail(self):
        address = Address.objects.get(id=self.request.GET.get("id"))
        data=json.dumps({
                    "code": 0,
                    "data": {
                        "address": address.address,
                        "areaStr": address.area,
                        "cityId": address.city_id,
                        "cityStr": address.city,
                        "code": "",
                        "dateAdd": address.date_update.strftime('%Y-%m-%d %H:%M:%S'),
                        "dateUpdate": address.date_update.strftime('%Y-%m-%d %H:%M:%S'),
                        "districtId": False,
                        "id": address.id,
                        "isDefault": address.is_default,
                        "linkMan": address.link_man,
                        "mobile": address.phone,
                        "provinceId": address.province_id,
                        "provinceStr": address.province,
                        "status": 0,
                        "statusStr": "",
                        "uid": self.app.id,
                        "userId": self.user.id
                    },
                    "msg": "success"
                })
        return HttpResponse(data)



