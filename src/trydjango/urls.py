"""trydjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import include, path
from django.conf.urls import url
from pages.views import (
    home_view
)
from products import views
from django.contrib.auth import views as auth_views #name for easy differentiation
from django.views.generic import TemplateView
from products import views
urlpatterns = [
    url(r'', include('products.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^$', views.products_list, name = 'home'), #remember to use as_view() to render view
    url(r'^report_bug/$', views.report_bug, name = 'report'),
    url(r'authentication/', TemplateView.as_view(template_name = 'login/index.html'), name = 'authentication'),
    url(r'^chat/', include('chat.api.urls', namespace = 'chat')),
    path('api-auth/', include('rest_framework.urls')),
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
    path('nusopenid/', include('nusopenid.urls', namespace = 'openid')),
]