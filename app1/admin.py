# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from models import *
# Register your models here.
class AppConfigAdmin(admin.ModelAdmin):
    list_display = ('sub_domain', 'mall_name')
    search_fields = ('sub_domain', 'mall_name')
 
class GoodsAdmin(admin.ModelAdmin):
    list_display = ('name',)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','key')

class BannerAdmin(admin.ModelAdmin):
    list_display = ('title',)

class PictureAdmin(admin.ModelAdmin):
    list_display = ('name','pic')

class OrderAdmin(admin.ModelAdmin):
    list_display = ('user','link_man','order_num','address','total','status','date','phone','remark')
    search_fields = ('status','date')
    list_filter = ('status','date')

class UserAdmin(admin.ModelAdmin):
    list_display = ('name','open_id')

admin.site.register(AppConfig,AppConfigAdmin)
admin.site.register(Goods,GoodsAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Banner,BannerAdmin)
admin.site.register(Picture,PictureAdmin)
admin.site.register(Order,OrderAdmin)
admin.site.register(WechatUser,UserAdmin)

admin.site.register([Address,AccessToken,Payment,Discount,Article])
admin.site.site_header = '简陋的后台管理系统'
admin.site.site_title = '简陋的后台管理系统'
