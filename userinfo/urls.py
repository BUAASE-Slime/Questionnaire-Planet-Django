from django.urls import path
from .views import *


urlpatterns = [
    path('login', login),
    path('register', register),
    path('logout', logout),
    path('confirm', user_confirm),
    path('unverified_email', unverified_email),
    path('change/password', change_passwords),

]
