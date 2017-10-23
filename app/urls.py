from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^config/get_value$', views.get_config_value),
    url(r'^user/check_token$', views.check_token),
    url(r'^user/wxapp/login$', views.login),
    #url(r'^/template_msg/put$', views.template_msg),
    url(r'^user/wxapp/register/complex$', views.register_cplx),
     
    url(r'^banner/list$', views.banner_list),
    #url(r'^/shop/goods/category/all$', views.template_msg),
    #url(r'^/shop/goods/list$', views.template_msg),
    #url(r'^/pages/goods-details/index', views.template_msg),


]
