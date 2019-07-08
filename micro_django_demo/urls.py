"""micro_django_demo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls import url
from rest_framework import permissions
from rest_framework.settings import api_settings
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.views.static import serve
import re
from micro_django_demo.settings import MICRO_VERSION

# import drf_yasg.generators.OpenAPISchemaGenerator  # schema生成器位置
schema_view = get_schema_view(
    openapi.Info(
        title="BookDemoAPI文档",  # 标题，总名字
        default_version=MICRO_VERSION,
        description="这是一个demo文档的描述",
        terms_of_service="http://www.baidu.com",   # api服务条款，是个链接指向
        contact=openapi.Contact(name="snow", email="zrs@rowenatech.com"),
        license=openapi.License(name="BSD License")
    ),
    # url="http://haha.xixi.com", # 这里不写，会去setting里边取 DEFAULT_API_URL（API base url, 如果留空，则将从提供view的位置推断出）
    public=True,
    authentication_classes=api_settings.DEFAULT_AUTHENTICATION_CLASSES,  # 默认是这个
    permission_classes=(permissions.AllowAny,)
)


# url == re_path，  path跟flask路由用法类型，用<int: age>   <str: name>
urlpatterns = [
    path('admin/', admin.site.urls),
    path("apis/", include("book_demo.urls")),
    # path("/<str:name>", ),
    # re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    url(r'^%s(?P<path>.*)$' % re.escape(settings.STATIC_URL.lstrip('/')), serve, {"document_root": settings.STATIC_ROOT})
]
