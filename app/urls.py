from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^config/get-value$', views.get_config_value),
    url(r'^user/check-token$', views.check_token),
    url(r'^user/wxapp/login$', views.login),
    #url(r'^/template_msg/put$', views.template_msg),
    url(r'^user/wxapp/register/complex$', views.register_cplx),
     
    url(r'^banner/list$', views.banner_list),
    url(r'^shop/goods/category/all$', views.all_category),
    url(r'^shop/goods/list$', views.goods_list),
    url(r'^shop/goods/detail$', views.goods_detail),

    url(r'^user/shipping-address/list$', views.address_list),
    url(r'^user/shipping-address/add$', views.address_add),
    url(r'^user/shipping-address/update$', views.address_update),
    url(r'^user/shipping-address/delete$', views.address_delete),
    url(r'^user/shipping-address/default$', views.address_default),
    url(r'^user/shipping-address/detail$', views.address_detail),

    url(r'^order/statistics$', views.order_statistics),
    url(r'^order/list$', views.order_list),
    url(r'^order/close$', views.order_close),
    url(r'^order/detail$', views.order_detail),
    url(r'^order/create$', views.order_create),

    url(r'^pay/wxapp/get-pay-data$', views.wxapp_pay),
    url(r'^pay/notify$', views.pay_notify),
]
