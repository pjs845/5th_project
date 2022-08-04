from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_page, name='main'),
    path('paging/', views.paging, name='paging'),
    path('signup/', views.signup, name='sugnup'),
    path('board/', views.board_page, name='board'),
    path('page2/', views.ad_page, name='page2'),
]