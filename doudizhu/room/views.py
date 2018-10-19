from django.shortcuts import render, HttpResponse,redirect
from index.views import islogin
from socket import *
from .models import *
from index.models import UserInfo
import json
from multiprocessing import Value,Lock
from time import sleep
import ctypes
import time
import re
# Create your views here.
# 同步房间信息共享内存字典{'room_id':<b'{'name_list':[],'user_name':{'img':'...','name':'...'}}'>}
D = {}
#创建房间
def createroom_views(request):
    if islogin(request):
        room_n = request.GET.get('roomname')
        rlist = Room.objects.filter(room_name=room_n)
        if rlist:
            return HttpResponse(json.dumps({'error':'房间已存在'}))
        else:
            try:
                room_root = request.session['uname']
                Room(room_name=room_n,room_root=room_root).save()
                roomobj = Room.objects.filter(room_name=room_n)[0]
                user = UserInfo.objects.get(uname = room_root)
                user.room_n = roomobj
                user.save()
            except:
                return HttpResponse(json.dumps({'error':'创建失败，请重试'}))
            # 创建共享内存
            Vobj = Value(ctypes.c_char_p,b"{'name_list':[]}")
            D[str(roomobj.id)] = Vobj
            Data_synchronization(request,roomobj.id)
            return HttpResponse(json.dumps({'id':roomobj.id}))
    else:
        return HttpResponse('404')
#获取房间页面
def getroom_views(request):
    if islogin(request):
        print('@@@@@@@@@@',D)
        id = request.GET.get('id')
        room_obj = Room.objects.filter(id=id)
        user = UserInfo.objects.get(id=request.session['id'])
        if room_obj:
            d = {
                'v':len(eval(D[id].value.decode()))-1,
                'name_list':eval(D[id].value.decode())['name_list']
            }
            dic = {
                'room_id':room_obj[0].id,
                'room_name':room_obj[0].room_name,
                'room_root':room_obj[0].room_root,
                'uimg':user.uimg.url,
                'uname':user.uname,
                'v':json.dumps(d)
            }
            return render(request,'room.html',dic)
        else:
            return HttpResponse('404')
    else:
        return redirect('/')
#加入房间
def joinroom_views(request):
    if islogin(request):
        roomname = request.GET.get('roomname')
        try:
            roomobj = Room.objects.get(room_name=roomname)
        except:
            return HttpResponse(json.dumps({'error':'没有这个房间'}))
        try:
            user = UserInfo.objects.get(id=request.session['id'])
            if user.room_n == roomobj or user.room_n != None:
                return HttpResponse(json.dumps({'error':'已经加入房间'}))
            user.room_n = roomobj
            user.save()
        except:
            return HttpResponse(json.dumps({'error':'加入失败，请重试'}))
        # 把要同步的数据放入共享内存
        Data_synchronization(request,roomobj.id)
        return HttpResponse(json.dumps({'id':roomobj.id}))
    else:
        return redirect('/')
#放入共享内存
def Data_synchronization(request,room_id):
    name = request.session['uname']
    user = UserInfo.objects.get(uname=name)
    img = user.uimg.url
    vobj = D[str(room_id)]
    d = eval(vobj.value.decode())
    d['name_list'].append(name)
    d[name] = {'img':img,'name':name}
    vobj.value = str(d).encode()
#获取房间数据
def getroomdata_views(request):
    if islogin(request):
        room_id = request.GET.get('room_id')
        room_root = request.GET.get('room_root')
        userlist = UserInfo.objects.filter(room_n=room_id)
        l = []
        for user in userlist:
            if user.uname != room_root:
                l.append(user.uname)
        jsonobj = json.dumps({'book':len(l),'data':l})
        return HttpResponse(jsonobj)
    else:
        return redirect('/')
#长连接
def longconnect_views(request):
    t = time.time()
    room_id = request.GET.get('room_id')
    v = eval(request.GET.get('v'))
    try:
        Vobj = D[str(room_id)]
    except:
        return HttpResponse(json.dumps({'error':'房间已失效'}))
    while True:
        # if time.time() - t >= 500:
        #     break
        dobj = eval(Vobj.value.decode())   #共享内存中的字典对象
        if len(dobj) -1 == 0:
            break
        if len(dobj)-1 == v['v']:
            sleep(1)
        elif len(dobj)-1 > v['v']:
            d = dobj[dobj['name_list'][-1]]
            name = d['name']
            img = d['img']
            d = {
                'lnorde':1,
                'name':name,
                'img':img,
                'v':str({'v':len(dobj)-1,'name_list':dobj['name_list']})
            }
            return HttpResponse(json.dumps(d))
        else:
            name_list = v['name_list']
            n = name_list[::]
            for i in dobj['name_list']:
                for r in name_list:
                    if r == i:
                        n.remove(i)
            d = {
                'lnorde':0,
                'name':n[0],
                'v':str({'v':len(dobj)-1,'name_list':dobj['name_list']})
            }
            return HttpResponse(json.dumps(d))
    # except:
    #     return HttpResponse(json.dumps({'error':'404'}))
    # return HttpResponse(json.dumps({'error':'超时'}))
#退出房间
def signout_views(request):
    id = request.session['id']
    name = request.session['uname']
    room_id = request.GET.get('room_id')
    nu = request.GET.get('nu')
    room_root = request.GET.get('room_root')
    try:
        # 初始化用户房间字段
        userlist = UserInfo.objects.filter(room_n=room_id)
        for i in userlist:
            i.room_n = None
            i.save()
    except:
        return HttpResponse(json.dumps({'error':'退出失败'}))
    if room_root:
        try:
            D.pop(str(room_id))
        except:
            pass
        roomobj = Room.objects.get(id=room_id)
        roomobj.delete()
    else:
        try:
            vobj = D[str(room_id)]
            dobj = eval(vobj.value.decode())
            dobj.pop(name)
            dobj['name_list'].remove(name)
            vobj.value = str(dobj).encode()
        except:
            pass
    return HttpResponse(json.dumps({'o':'k'}))