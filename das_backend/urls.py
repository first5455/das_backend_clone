"""das_backend URL Configuration

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
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from api.views.WebpageView import home
from os import environ
from dotenv import load_dotenv

load_dotenv()

def getSchemaView():
    try:
        envUrl = environ['API_URL']
        schema_view = get_schema_view(
            openapi.Info(
                title="D.A.S API",
                default_version='v1',
                description="Api Documentation",
            ),
            public=True,
            url=envUrl,
            permission_classes=(permissions.AllowAny,),
        )
        return schema_view
    except KeyError:
        schema_view = get_schema_view(
            openapi.Info(
                title="D.A.S API",
                default_version='v1',
                description="Api Documentation",
            ),
            public=True,
            permission_classes=(permissions.AllowAny,),
        )
        return schema_view

urlpatterns = [
                  path('swagger/', getSchemaView().with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
                  path('redoc/', getSchemaView().with_ui('redoc', cache_timeout=0), name='schema-redoc'),
                  path('api/v1/', include('api.urls')),
                  path('', home),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
