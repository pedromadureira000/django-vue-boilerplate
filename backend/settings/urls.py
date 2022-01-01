"""URL Configuration

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
#  from django.conf.urls import url # this is deprecated in django 4.0
from django.contrib import admin
from django.urls import path, include, re_path
from core.views import apiNotFound
from django.conf import settings
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

urlpatterns = [
    path('api/user/', include('core.urls')),
] 

if settings.DEBUG:
    urlpatterns +=  path('admin/', admin.site.urls),
    #  urlpatterns += [re_path(r'^api/.*$', apiNotFound )]   # this is causing swagger fetch error 

    schema_view = get_schema_view(
       openapi.Info(
          title="API Documentation",
          default_version='v1',
          description="API from django-vue Scaffold",
          terms_of_service="https://www.google.com/policies/terms/",
          contact=openapi.Contact(email="contato@phsolucoesweb.com.br"),
          license=openapi.License(name="No License"),
       ),
       public=True, #if False, includes only endpoints the current user has access to
       permission_classes=(permissions.AllowAny,), 
    )
    #Swagger
    urlpatterns += [
       #  url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
       #  url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
       #  url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
       #  path('swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
       path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
       path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    ]
