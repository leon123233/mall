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

    url(r'^user/shipping-address/list$', views.address_list),
    url(r'^user/shipping-address/add$', views.address_add),
    url(r'^user/shipping-address/update$', views.address_update),
    url(r'^user/shipping-address/delete$', views.address_delete),
    url(r'^user/shipping-address/default$', views.address_default),
    url(r'^user/shipping-address/detail$', views.address_detail),
]
