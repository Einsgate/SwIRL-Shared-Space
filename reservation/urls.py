from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    
    path('accounts/login', views.accounts_login, name='cas_ng_login'),
    path('accounts/logout', views.accounts_logout, name='cas_ng_logout'),
    
    path('index.html', views.index, name='index_html'),
    path('reservation/index', views.index, name='reservation_index'),
    path('reservation/index.html', views.index, name='reservation_index_html'),
    path('reservation/list', views.reservation_list, name='reservation_list'),
    path('reservation/history', views.reservation_history, name='reservation_history'),  
    path('reservation/create', views.reservation_create, name='reservation_create'),
    path('reservation/delete', views.reservation_delete, name='reservation_delete'),
    path('zone/list', views.zone_list, name='zone_list'),
]