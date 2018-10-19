from django.shortcuts import render, redirect,HttpResponse
from .models import *
import json
# Create your views here.
#判断用户是否登录
def islogin(request):
        if 'id' in request.session and 'uname' in request.session:
            if UserInfo.objects.filter(id=request.session['id'], isActiv=True):
                return True
        if 'id' in request.COOKIES and 'uname' in request.COOKIES:
            if UserInfo.objects.filter(id=request.COOKIES['id'], isActiv=True):
                request.session['id'] = request.COOKIES['id']
                request.session['uname'] = request.COOKIES['uname']
                return True
#注册
def register_views(request):
    if request.method == 'GET':
        return render(request,'register.html')
    elif request.method == 'POST':
        uname = request.POST.get('uname')
        if UserInfo.objects.filter(uname=uname):
            return render(request,'register.html',{'error':'用户名已存在'})
        upwd = request.POST.get('upwd')
        cpwd = request.POST.get('cpwd')
        if upwd != cpwd :
            return render(request,'register.html',{'error':'两次密码不一致'})
        uphone = request.POST.get('uphone')
        if UserInfo.objects.filter(uphone=uphone):
            return render(request,'register.html',{'error':'一个号码只能注册一个账号'})
        uimg = request.FILES.get('uimg')
        if not uimg:
            uimg = 'touxiang/touxiang.jpg'
        try:
            UserInfo(uname=uname,uimg=uimg,uphone=uphone,upwd=upwd).save()
        except:
            return render(request,'register.html',{'error':'注册失败请重试'})
        request.session['id'] = UserInfo.objects.filter(uname=uname)[0].id
        request.session['uname'] = UserInfo.objects.filter(uname=uname)[0].uname
        request.session.set_expiry(0)
        return redirect('/index')
#主页
def index_views(request):
    if request.method == 'GET':
        if islogin(request):
            user = UserInfo.objects.filter(id=request.session['id'])[0]
            data = {
                'uimg':user.uimg.url,
                'uname':user.uname,
                'ucoin':user.ucoin,
            }
            return render(request,'index.html',data)
        else:
            return redirect('/')
#登录
def login_views(request):
    if request.method == 'GET':
        if islogin(request):
            return redirect('/index')
        return render(request,'login.html')
    elif request.method == 'POST':
        uphone = request.POST.get('uphone')
        upwd = request.POST.get('upwd')
        user = UserInfo.objects.filter(uphone=uphone, upwd=upwd)
        if user:
            user = user[0]
            user.save()
            url = HttpResponse(json.dumps({'status':'1'}))
            request.session['id'] = user.id
            request.session['uname'] = user.uname
            if request.POST['apwd'] == 'T' :
                url.set_cookie('id',user.id,60*60*24*366)
                url.set_cookie('uname',user.uname,60*60*24*366)
                return url
            else:
                return HttpResponse(json.dumps({'status':'0'}))
        else:
            dic = {
                'error':'手机号或密码错误',

            }
            print(json.dumps(dic))
            return HttpResponse(json.dumps(dic))
#退出
def tuichu_views(request):
    del request.session['id']
    del request.session['uname']
    html = redirect('/')
    html.delete_cookie('id')
    html.delete_cookie('uname')
    return html

#name Ajax 验证
def name_Ajax_views(request):
    print('66666')
    if request.method == 'GET':
        name = request.GET.get('uname')
        user = UserInfo.objects.filter(uname=name)
        if user:
            return HttpResponse(json.dumps({'data':0}))
        else:
            print(321)
            return HttpResponse(json.dumps({'data':1}))
    else:
        return HttpResponse('404')