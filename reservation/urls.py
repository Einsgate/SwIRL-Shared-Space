from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.index, name='index'),

    #path('login', views.accounts_login, name='cas_ng_login'),
    #path('accounts/logout', views.accounts_logout, name='cas_ng_logout'),

    path('index.html', views.index, name='index_html'),
    #user mngment
    path('usermng/staff', views.usermng_staff, name='staff_index'),
    path('usermng/leader', views.usermng_leader, name='leader_index'),
    path('usermng/member', views.usermng_member, name='member_index'),
    path('usermng/deleteByRole', views.user_delete, name='user_delete'),
    path('usermng/authUser', views.authority_user, name='authority_user'),
    re_path('usermng/authUserDetail/(\d+)/', views.authority_detail, name='authority_detail'),
    path('usermng/authUserUpdate', views.authority_udpate, name='authority_update'),

    #reservation
    path('reservation/index', views.index, name='reservation_index'),
    path('reservation/index.html', views.index, name='reservation_index_html'),
    path('reservation/list', views.reservation_list, name='reservation_list'),
    path('reservation/history', views.reservation_history, name='reservation_history'),  
    path('reservation/create', views.reservation_create, name='reservation_create'),
    path('reservation/delete', views.reservation_delete, name='reservation_delete'),
    path('zone/list', views.zone_list, name='zone_list'),

    # team
    path('team/view', views.team_view, name='team_view'), 
    path('team/view/<int:team_id>/', views.team_detail, name='team_detail'), 
    path('team/view/<int:team_id>/update', views.team_details_update, name='team_details_update'), 
    path('team/delete', views.team_delete, name='team_delete'),
    path('team/create', views.team_create, name='team_create'), 
    path('training/view', views.training_view, name='training_view'),
    path('training/delete', views.training_delete, name='training_delete'),
    path('training/create', views.training_create, name='training_create'),
]