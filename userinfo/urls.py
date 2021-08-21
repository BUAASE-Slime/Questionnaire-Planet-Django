from django.conf.urls.static import static
from django.urls import path
from userinfo.views import *


urlpatterns = [
    path('login', login),
    path('register', register),
    path('logout', logout),
    path('confirm/', user_confirm),
    path('unverified_email', unverified_email),

]
