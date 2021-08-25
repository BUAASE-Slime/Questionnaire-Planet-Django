from django.urls import path
from .views import *


urlpatterns = [
    path('login', login),
    path('register', register),
    path('logout', logout),
    path('confirm/email', user_confirm),
    path('send_verify_email', send_unverified_email),

    path('change/email', change_email),
    path('change/password', change_password),
    path('send/code', send_code),
    path('get/userinfo', get_userinfo),

    path('confirm/userinfo', confirm_userinfo),
]
