from django.conf.urls import url
from .views import *
urlpatterns = [
    # 开始游戏
    url(r'^page',ispage_views),
    # 长连接,等待游戏开始
    url(r'^long_connect',long_connect_views),
    # 获取游戏页面
    url(r'^getpage',get_page_views),
    # 长连接，获取扑克
    url(r'^get_puke_accept',get_puke_accept_views),
    # 出牌
    url(r'^appear_puke',appear_puke_views),
    #结束游戏
    url(r'^game_over',game_over_views),
]