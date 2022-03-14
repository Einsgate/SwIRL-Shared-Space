from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('reservation/index', views.index, name='reservation_index'),
    path('reservation/list', views.reservation_list, name='reservation_list'),
    path('reservation/create', views.reservation_create, name='reservation_create'),
    path('zone/list', views.zone_list, name='zone_list'),
]