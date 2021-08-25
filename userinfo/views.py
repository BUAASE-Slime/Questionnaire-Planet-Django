import random

from django.conf import settings
from django.http import JsonResponse
import re
import datetime
import pytz
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

from userinfo.models import ConfirmString
from utils.sendEmail import *
from userinfo.models import User

from .form import *

utc = pytz.UTC


# Create your views here.

@csrf_exempt
@api_view(['POST'])
def login(request):
    if request.session.get('is_login'):  # login repeatedly not allowed
        return JsonResponse({'status_code': 2})

    login_form = LoginForm(request.POST)

    if login_form.is_valid():
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            return JsonResponse({'status_code': 3})

        if user.password == hash_code(password):
            request.session['is_login'] = True
            request.session['username'] = username

            print(username + " 登录成功")

            if not user.has_confirmed:
                return JsonResponse({'status_code': 5})

            return JsonResponse({'status_code': 1})

        else:
            return JsonResponse({'status_code': 4})

    return JsonResponse({'status_code': -1})


@csrf_exempt
def register(request):
    register_form = RegisterForm(request.POST)

    if register_form.is_valid():
        username = register_form.cleaned_data.get('username')
        password1 = register_form.cleaned_data.get('password1')
        password2 = register_form.cleaned_data.get('password2')
        email = register_form.cleaned_data.get('email')

        same_name_user = User.objects.filter(username=username)
        if same_name_user:
            return JsonResponse({'status_code': 2})

        same_email_user = User.objects.filter(email=email)
        if same_email_user:
            return JsonResponse({'status_code': 3})

        # 检测密码不符合规范：8-18，英文字母+数字
        if not re.match('^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{8,18}$', password1):
            return JsonResponse({'status_code': 4})

        if password1 != password2:
            return JsonResponse({'status_code': 5})

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
            return JsonResponse({'status_code': 6})

        return JsonResponse({'status_code': 1})

    else:
        return JsonResponse({'status_code': -1})


@csrf_exempt
def logout(request):
    if not request.session.get('is_login', None):
        return JsonResponse({'status_code': 401})

    print(request.session.get('is_login'))

    request.session.flush()
    return JsonResponse({'status_code': 200})


@csrf_exempt
def user_confirm(request):
    if request.method == 'POST':
        code = request.POST.get('code')  # get code from url (?code=..)
        try:
            confirm = ConfirmString.objects.get(code=code)
        except:
            return JsonResponse({'status_code': 2})

        c_time = confirm.c_time.replace(tzinfo=utc)
        now = datetime.datetime.now().replace(tzinfo=utc)
        if now > c_time + datetime.timedelta(settings.CONFIRM_DAYS):
            confirm.user.delete()
            return JsonResponse({'status_code': 3})
        else:
            confirm.user.has_confirmed = True
            confirm.user.save()
            confirm.delete()
            return JsonResponse({'status_code': 1})


@csrf_exempt
def send_unverified_email(request):
    try:
        this_user = User.objects.get(username=request.session['username'])
    except:
        return JsonResponse({'status_code': 2})

    if this_user.has_confirmed:
        return JsonResponse({'status_code': 3})

    try:
        code = ConfirmString.objects.get(user_id=this_user.id).code
        send_email_confirm(this_user.email, code)
    except:
        this_user.delete()
        return JsonResponse({'status_code': 4})

    return JsonResponse({'status_code': 1})


@csrf_exempt
def change_email(request):
    email = request.POST.get("email")
    code = request.POST.get("code")

    if User.objects.filter(email=email):
        return JsonResponse({'status_code': 4})

    try:
        confirm = ConfirmString.objects.get(code=code)
    except:
        return JsonResponse({'status_code': 2})

    c_time = confirm.c_time.replace(tzinfo=utc)
    now = datetime.datetime.now().replace(tzinfo=utc)
    if now > c_time + datetime.timedelta(settings.CONFIRM_DAYS):
        return JsonResponse({'status_code': 3})
    else:
        confirm.user.has_confirmed = True
        confirm.user.email = email
        confirm.user.save()
        confirm.delete()
        return JsonResponse({'status_code': 1})


@csrf_exempt
def send_code(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        if User.objects.filter(email=email):
            return JsonResponse({'status_code': 4})

        user = User.objects.get(username=request.session.get('username'))
        code = ""
        for i in range(6):
            ch = chr(random.randrange(ord('0'), ord('9') + 1))
            code += ch

        if ConfirmString.objects.filter(user=user):
            cs = ConfirmString.objects.get(user=user)
            cs.delete()

        ConfirmString.objects.create(code=code, user=user, )
        print(user.username + "申请更改邮箱地址，生成随机码为 " + code)

        try:
            send_email_change_confirm(email=email, code=code)
            return JsonResponse({'status_code': 1})
        except:
            return JsonResponse({'status_code': 2})
    return JsonResponse({'status_code': 3})


@csrf_exempt
def change_password(request):
    if request.method == 'POST':
        password_form = ChangePasswordForm(request.POST)
        if password_form.is_valid():
            try:
                this_user = User.objects.get(username=request.session['username'])
            except:
                return JsonResponse({'status_code': 0})
            old_password = password_form.cleaned_data.get('old_password')
            new_password_1 = password_form.cleaned_data.get('new_password_1')
            new_password_2 = password_form.cleaned_data.get('new_password_2')
            if this_user.password != hash_code(old_password):
                return JsonResponse({'status_code': 4})
            if new_password_1 != new_password_2:
                response = {'status_code': 2, 'message': '两次输入的密码不同'}
                return JsonResponse(response)
            # 检测密码不符合规范：8-18，英文字母+数字
            if not re.match('^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{8,18}$', new_password_1):
                return JsonResponse({'status_code': 5})
            if new_password_1 == old_password:
                response = {'status_code': 3, 'message': '新旧密码相同'}
                return JsonResponse(response)
            this_user.password = hash_code(new_password_1)
            this_user.save()
            return JsonResponse({'status_code': 1, 'message': 'success'})

        else:
            response = {'status_code': -1, 'message': 'invalid form'}
            return JsonResponse(response)
    else:
        response = {'status_code': -2, 'message': '请求错误'}
        return JsonResponse(response)


@csrf_exempt
def get_userinfo(request):
    if not request.session.get('is_login'):
        return JsonResponse({'status_code': 3})
    username = request.session.get('username')
    print(username + " 请求进入账户设置页面")
    try:
        user = User.objects.get(username=username)
    except:
        print(username + " 进入账户设置页面失败，将清除前端登录信息")
        return JsonResponse({'status_code': 2})
    print(user.username + " 成功进入账户设置页面")
    return JsonResponse({'status_code': 1, 'username': user.username, 'is_confirmed': user.has_confirmed, 'email': user.email})


@csrf_exempt
def confirm_userinfo(request):
    username = request.POST.get('username')
    print(username + " 请求验证登录信息")
    try:
        username_backend = request.session['username']
        print("后端存储用户名为 " + username_backend + ", 前端存储用户名为 " + username)
        if username_backend != username:
            print(username + " 验证登录信息失败，将强制退出登录")
            request.session.flush()
            return JsonResponse({'status_code': 2})
    except:
        print(username + " 验证登录信息失败，将强制退出登录")
        request.session.flush()
        return JsonResponse({'status_code': 2})
    else:
        print(username + " 验证登录信息成功")
        return JsonResponse({'status_code': 1})
