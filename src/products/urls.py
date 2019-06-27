from django.conf.urls import url
from django.urls import path
from django.contrib import admin
from django.contrib.auth import views as auth_views #name for easy differentiation

from django.views.generic import TemplateView

from products import views
urlpatterns = [
    #url(r'^$', views.Home.as_view(), name = 'home'), #remember to use as_view() to render view
    url(r'^$', views.products_list, name = 'home'), #remember to use as_view() to render view

    #create C:
    url(r'^post/create/$', views.PostCreate.as_view(), name = 'product-create'),

    #read R:
    url(r'^post/(?P<pk>[\d]+)/$', views.PostDetail.as_view(), name = 'product-detail'), #learn regex

    #update U:
    path('post/<int:id>/update/', views.product_update, name = 'product-update'),
    
    #delete D:
    path('post/<int:id>/delete/', views.product_delete_view, name = 'product-delete'),

    #authentication:
    url(r'^login/$', auth_views.LoginView.as_view(template_name = 'products/login.html'), name = 'login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name = 'logout'),

    #category:
    url(r'^post/category/(?P<pk>[\d]+)/$', views.PostCategory.as_view(), name = 'product-by-category'),
]