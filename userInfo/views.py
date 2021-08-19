from django.conf import settings
from django.http import JsonResponse
import re
import datetime
import pytz
from django.views.decorators.csrf import csrf_exempt
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework.views import APIView

from userInfo.form import *
from userInfo.models import ConfirmString
from utils.responseCode import *
from utils.sendEmail import make_confirm_string, send_email_confirm
from utils.toHash import hash_code

from rest_framework import viewsets

from userInfo.models import User

utc = pytz.UTC


# Create your views here.

class Params:
    username = openapi.Parameter('username', openapi.TYPE_STRING, description='用户名', type=openapi.TYPE_STRING)
    password = openapi.Parameter('password', openapi.TYPE_STRING, description='密码', type=openapi.TYPE_STRING)
    password1 = openapi.Parameter('password1', openapi.TYPE_STRING, description='密码', type=openapi.TYPE_STRING)
    password2 = openapi.Parameter('password2', openapi.TYPE_STRING, description='确认密码', type=openapi.TYPE_STRING)
    email = openapi.Parameter('email', openapi.TYPE_STRING, description='邮箱地址', type=openapi.TYPE_STRING)


@csrf_exempt
@swagger_auto_schema(method='post',
                     # request_body=openapi.Schema(
                     #     type=openapi.TYPE_OBJECT,
                     #     required=['username', 'password'],
                     #     properties={
                     #         'username': openapi.Schema(type=openapi.TYPE_STRING),
                     #         'password': openapi.Schema(type=openapi.TYPE_STRING)
                     #     }
                     # ),
                     responses={200: '登录成功', 401: '用户重复登录', 402: '用户名不存在', 403: '密码错误', 404: '用户未经过邮箱确认', 405: '表单错误'},
                     manual_parameters=[Params.username, Params.password]
                     )
@api_view(['POST'])
def login(request):
    if request.session.get('is_login', None):  # login repeatedly not allowed
        return JsonResponse({'status_code': 401})

    login_form = LoginForm(request.POST)

    if login_form.is_valid():
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            return JsonResponse({'status_code': 402})

        if user.password == password:
            request.session['is_login'] = True
            request.session['username'] = username

            if not user.has_confirmed:
                return JsonResponse({'status_code': 404})

            return JsonResponse({'status_code': 200})

        else:
            return JsonResponse({'status_code': 403})

    return JsonResponse({'status_code': 405})


@csrf_exempt
@swagger_auto_schema(method='post',
                     responses={200: '注册成功', 401: '用户名已存在', 402: '邮箱已注册或不可用', 403: '密码不符合规则，至少同时包含字母和数字，且长度为 8-18', 404: '两次输入的密码不同', 405: '邮件验证码发送失败', 406: '表单格式错误'},
                     manual_parameters=[Params.username, Params.email, Params.password1, Params.password2]
                     )
@api_view(['POST'])
def register(request):
    register_form = RegisterForm(request.POST)

    if register_form.is_valid():
        username = register_form.cleaned_data.get('username')
        password1 = register_form.cleaned_data.get('password1')
        password2 = register_form.cleaned_data.get('password2')
        email = register_form.cleaned_data.get('email')

        same_name_user = User.objects.filter(username=username)
        if same_name_user:
            return JsonResponse({'status_code': 401})

        same_email_user = User.objects.filter(email=email)
        if same_email_user:
            return JsonResponse({'status_code': 402})

        # 检测密码不符合规范：8-18，英文字母+数字
        if not re.match('^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{8,18}$', password1):
            return JsonResponse({'status_code': 403})

        if password1 != password2:
            return JsonResponse({'status_code': 404})

        # 成功
        new_user = User()
        new_user.username = username
        new_user.password = hash_code(password1)
        new_user.email = email
        new_user.save()

        request.session['is_login'] = True
        request.session['username'] = username

        code = make_confirm_string(new_user)
        try:
            send_email_confirm(email, code)
        except:
            new_user.delete()
            return JsonResponse({'status_code': 405})

        return JsonResponse({'status_code': 200})

    else:
        return JsonResponse({'status_code': 406})


@csrf_exempt
def logout(request):
    if not request.session.get('is_login', None):
        return JsonResponse({'status_code': LogoutStatus.USER_NOT_LOGIN})

    request.session.flush()
    return JsonResponse({'status_code': SUCCESS})


@csrf_exempt
def user_confirm(request):
    if request.method == 'POST':
        code = request.POST.get('code')  # get code from url (?code=..)
        try:
            confirm = ConfirmString.objects.get(code=code)
        except:
            return JsonResponse({'status_code': ConfirmStatus.STRING_MISS})

        c_time = confirm.c_time.replace(tzinfo=utc)
        now = datetime.datetime.now().replace(tzinfo=utc)
        if now > c_time + datetime.timedelta(settings.CONFIRM_DAYS):
            confirm.user.delete()
            return JsonResponse({'status_code': ConfirmStatus.CONFIRM_EXPIRED})
        else:
            confirm.user.has_confirmed = True
            confirm.user.save()
            confirm.delete()
            return JsonResponse({'status_code': SUCCESS})

    return JsonResponse({'status_code': DEFAULT})


@csrf_exempt
def unverified_email(request):
    try:
        this_user = User.objects.get(username=request.session['username'])
    except:
        return JsonResponse({'status_code': VerifyStatus.USER_NOT_LOGIN})

    if this_user.has_confirmed:
        return JsonResponse({'status_code': VerifyStatus.CONFIRM_REPEATED})

    try:
        code = ConfirmString.objects.get(user_id=this_user.id).code
        send_email_confirm(this_user.email, code)
    except:
        this_user.delete()
        return JsonResponse({'status_code': VerifyStatus.SEND_EMAIL_ERROR})

    return JsonResponse({'status_code': SUCCESS, 'email': this_user.email, 'username': this_user.username})
