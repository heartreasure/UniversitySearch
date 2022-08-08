import random

from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse
from django.shortcuts import render, redirect

from django.views.decorators.csrf import csrf_exempt

# Create your views here.
from django.urls import reverse

from index.models import MyUser, FeedbackInfo
from django.contrib.auth.decorators import login_required


# 主页
def indexView(request):
    return render(request, 'index.html', locals())


def featureView(request):
    return render(request, 'feature.html', locals())


# 登录
def userLogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember = request.POST.get('remember')
        if MyUser.objects.filter(username=username):
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    next_url = request.GET.get('next', reverse('index'))
                    response = redirect(next_url)
                    if remember == "on":
                        # 设置cookie username *过期时间为1周
                        response.set_cookie('username', username, max_age=7 * 24 * 3600)
                    else:
                        response.delete_cookie('username')
                    return response
            else:
                tips = '账号密码错误，请重新输入'
        else:
            tips = '用户不存在，请注册'
    else:
        if 'username' in request.COOKIES:
            # 获取记住的用户名
            username = request.COOKIES['username']
        else:
            username = ''
    return render(request, 'signin.html', locals())


# 注册
def userRegister(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if MyUser.objects.filter(username=username):
            tips = '用户已存在'
        else:
            user_info = {
                'username': username, 'password': password,
                'email': email,
                'is_superuser': 1, 'is_staff': 1
            }
            user = MyUser.objects.create_user(**user_info)
            user.save()
            tips = '注册成功，请登录'
            logout(request)
            return render(request, 'signup_success.html', locals())

    return render(request, 'signup.html', locals())


# 注销
def logoutView(request):
    logout(request)
    return redirect(reverse('index'))


# 联系我们
@csrf_exempt
def contactView(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        type = request.POST.get('subject')
        message = request.POST.get('message')
        newInfo = FeedbackInfo(name=name, email=email, type=type, info=message)
        newInfo.save()
        return render(request, 'feedback_success.html', locals())
    return render(request, 'contact.html', locals())


# 找回密码
def findpsView(request):
    button = '获取验证码'
    VCodeInfo = False
    password = False
    error_tips = ''
    if request.method == 'POST':
        u = request.POST.get('username')
        VCode = request.POST.get('VCode', '')
        p = request.POST.get('password')
        user = MyUser.objects.filter(username=u)
        # 用户不存在
        if not user:
            error_tips = '用户 ' + u + ' 不存在'
        else:
            # 判断验证码是否已发送
            if not request.session.get('VCode', ''):
                # 发送验证码并写入session
                button = '重置密码'
                right_tips = '验证码已发送'
                password = True
                VCodeInfo = True
                VCode = str(random.randint(1000, 9999))
                request.session['VCode'] = VCode
                message = '您的验证码为：' + VCode
                user[0].email_user('找回密码', message)
            elif VCode == request.session.get('VCode'):
                dj_ps = make_password(p, None, 'pbkdf2_sha256')
                user[0].password = dj_ps
                user[0].save()
                del request.session['VCode']
                right_tips = '密码已重置'
                return render(request, 'reset_success.html', locals())
            else:
                error_tips = '验证码错误，请重新获取'
                VCodeInfo = False
                password = False
                del request.session['VCode']
    return render(request, 'reset_ps.html', locals())
