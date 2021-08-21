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

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

import Qn.views

schema_view = get_schema_view(
    # 具体定义详见 [Swagger/OpenAPI 规范](https://swagger.io/specification/#infoObject "Swagger/OpenAPI 规范")
    openapi.Info(
        title="Snippets API",
        default_version='v1.0.0',
        description="Test description",
        terms_of_service="https://blog.zewan.cc/",
        contact=openapi.Contact(email="huangzehuan@buaa.edu.cn"),
        license=openapi.License(name="BSD License"),
    ),
    # public 表示文档完全公开, 无需针对用户鉴权
    public=True,
    # 可以传递 drf 的 BasePermission
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # drf_yasg
    re_path('^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-spec'),
    path('api/qs/swagger', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/qs/docs', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path('api/qs/admin/', admin.site.urls),
    path('api/qs/user/', include(('userinfo.urls', 'userinfo'))),
    path('api/qs/qn/', include(('Qn.urls', 'Qn'))),
    path('api/qs/all_count/submit', Qn.views.all_submittion_count),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


