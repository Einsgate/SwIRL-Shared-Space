from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
<<<<<<< HEAD
    path('list', views.reservation_list, name='list'),
=======
    path('create/', views.reservation_create, name='reservation_create'),
>>>>>>> dev
]