from django.shortcuts import render,HttpResponse
from index.views import islogin
from room.models import *
from index.models import *
import json
from time import sleep
from multiprocessing import Value
import ctypes
from .models import *
from random import shuffle
# Create your views here.
# 开始游戏的共享内存字典
game_D = {}
# 判断游戏是否可以开始
def ispage_views(request):
    if islogin(request):
        # 创建或加入等待游戏开始的共享内存
        join_memory(request)
        room_id = request.GET.get('room_id')
        vobj = game_D[str(room_id)]
        if int(vobj.value.decode()) == 3:
            set_up_data(room_id)
            game_D.pop(room_id)
            return HttpResponse(json.dumps({'room_id':room_id}))
        else:
            return HttpResponse(json.dumps({'error':'人数不足'}))
# 创建游戏数据
def set_up_data(room_id):
    userlist = UserInfo.objects.filter(room_n=room_id)
    roomobj = Room.objects.get(id=room_id)
    puke_l = deal()
    a = 0
    for i in userlist:
        Game(room_id=roomobj,serial_number=a,user_id=i,brand=str(puke_l[a])).save()
        a += 1
# 长连接,等待游戏开始
def long_connect_views(request):
    join_memory(request)
    id = request.session['id']
    room_id = request.GET.get('room_id')
    vobj = game_D[room_id]
    while True:
        if int(vobj.value.decode()) != 3:
            sleep(1)
        else:
            d = {
                'room_id':room_id
            }
            return HttpResponse(json.dumps(d))
# 创建或加入等待游戏开始的共享内存
def join_memory(request):
    room_id = request.GET.get('room_id')
    try:
        vobj = game_D[str(room_id)]
        vobj.value = str(int(vobj.value)+1).encode()
    except:
        vobj = Value(ctypes.c_char_p,b'1')
        game_D[str(room_id)] = vobj
# 获取游戏页面
def get_page_views(request):
    if islogin(request):
        room_id = request.GET.get('room_id')
        uname = request.session['uname']
        uid = request.session['id']
        gameobj_l = Game.objects.filter(room_id=room_id)
        gameobj_list = []
        for i in gameobj_l:
            gameobj_list.append(i)
        gameobj = ''
        for userobj in gameobj_list:
            if userobj.user_id.id == uid:
                gameobj = userobj
                gameobj_list.remove(userobj)
        d = {
            'room_id':room_id,
            #导航栏信息
            'uname':gameobj.user_id.uname,
            'uimg':gameobj.user_id.uimg.url,
            'ucoin':gameobj.user_id.ucoin,
            'room_name':gameobj.room_id.room_name,
            #我的信息
            'puke':eval(gameobj.brand),
            'my_number':gameobj.serial_number,
            #玩家2信息
            'name2':gameobj_list[0].user_id.uname,
            'len_puke2':eval(gameobj_list[0].brand),
            'number2':gameobj_list[0].serial_number,
            #玩家3信息
            'name3':gameobj_list[1].user_id.uname,
            'len_puke3':eval(gameobj_list[1].brand),
            'number3': gameobj_list[1].serial_number,
        }
        return render(request,'game.html',d)
# 生成扑克
def puke():
    l = ['A','2','3','4','5','6','7','8','9','10','J','Q','K']
    l1 = ['大王','小王']
    for i in l:
        l1.append('♣'+i)
        l1.append('♠'+i)
        l1.append('♥'+i)
        l1.append('♦'+i)
    return l1
# 打乱牌堆
def deal():
    l = puke()
    shuffle(l)
    l1 = l[0:17]
    l2 = l[17:34]
    l3 = l[34:51]
    l4 = l[51:]
    l5 = [l1,l2,l3+l4]
    shuffle(l5)
    return l5
#扑克的共享内存字典
puke_D = {}
# 出牌
def appear_puke_views(request):
    if islogin(request):
        pukepart = request.GET.get('puke')
        uid = request.session['id']
        gameobj = Game.objects.get(user_id=uid)
        pukepart_list = pukepart.split(',')
        pukeall_list = eval(gameobj.brand)
        game_over = 0
        #游戏结束判定
        if len(pukepart_list) == len(pukeall_list):
            room_id = request.GET.get('room_id')
            gameobj_list = Game.objects.filter(room_id=room_id)
            gameobj_list.delete()
            game_over = gameobj.room_id.id
            join_puke(request, pukepart, game_over)  # 创建或加入或同步数据
        else :
            join_puke(request, pukepart, game_over)  # 创建或加入或同步数据
            for pukepart in pukepart_list:
                for pukeall in pukeall_list:
                    if pukepart == pukeall:
                        pukeall_list.remove(pukeall)
            gameobj.brand = pukeall_list
            gameobj.save()
        return HttpResponse(json.dumps({'o':'k'}))
#加入或创建或更新扑克数据
def join_puke(request,puke,game_over):
    room_id = request.GET.get('room_id')
    appear = request.GET.get('appear')
    puke_len = request.GET.get('puke_len')

    try:
        vobj = puke_D[str(room_id)]
        vobj.value = str({'appear':appear,'puke':puke,'puke_len':puke_len,'game_over':game_over}).encode()
    except:
        vobj = Value(ctypes.c_char_p,str({'appear':appear,'puke':puke,'puke_len':puke_len,'game_over':game_over}).encode())
        puke_D[str(room_id)] = vobj
# 同步扑克数据的长连接
def get_puke_accept_views(request):
    room_id = request.GET.get('room_id')
    appear = request.GET.get('appear')
    puke = request.GET.get('puke')
    while True:
        try:
            vobj = puke_D[str(room_id)]
        except:
            sleep(1.5)
            continue
        if eval(vobj.value.decode())['puke'] != puke:
            return HttpResponse(json.dumps(eval(vobj.value.decode())))
        else:
            sleep(1)
# 游戏结束
def game_over_views(request):
    try:
        room_id = request.GET.get('room_id')
        print('清除')
        game_D.pop(room_id)
    except:
        pass
    return HttpResponse(json.dumps({'o':'k'}))