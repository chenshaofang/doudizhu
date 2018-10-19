from django.conf.urls import url
from .views import *
urlpatterns = [
    #创建房间
    url(r'^createroom',createroom_views),
    #加入房间
    url(r'^joinroom',joinroom_views),
    #获取房间
    url(r'^getroom',getroom_views),
    #获取房间数据
    url(r'^get_room_data',getroomdata_views),
    #保持长连接
    url(r'^long_connect',longconnect_views),
    #退出房间
    url(r'^signout',signout_views),
]