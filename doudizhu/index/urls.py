from django.conf.urls import url
from .views import *
urlpatterns = [
    # 登录
    url(r'^$',login_views),
    #注册
    url(r'^register',register_views),
    #主页
    url(r'^index',index_views),
    #退出
    url(r'^tuichu',tuichu_views),
    #name Ajax 验证
    url(r'^name_Ajax',name_Ajax_views),
    # url(r'^getindexdata',getindex_views),
]
