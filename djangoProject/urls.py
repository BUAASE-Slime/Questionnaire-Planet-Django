"""djangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path

from django.conf.urls import url
from django.views.static import serve

import Qn.views

urlpatterns = [
    path('api/qs/admin/', admin.site.urls),
    path('api/qs/user/', include(('userinfo.urls', 'userinfo'))),
    path('api/qs/qn/', include(('Qn.urls', 'Qn'))),
    path('api/qs/sm/', include(('Submit.urls', 'Submit'))),
    path('api/qs/all_count/submit', Qn.views.all_submittion_count),

    url(r'media/(?P<path>.*)',serve,{'document_root':settings.MEDIA_ROOT}),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


