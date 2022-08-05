from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_page, name='main'),
    path('paging/', views.paging, name='paging'),
    path('signup/', views.signup, name='signup'),
    path('signup/signup_ok', views.signup_ok, name = 'signup_ok'),
    path('board/', views.board_page, name='board'),
    path('notice/', views.notice, name='notice'),
    path('page2/', views.ad_page, name='page2'),
]