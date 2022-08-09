from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_page, name='main'),
    path('paging/', views.paging, name='paging'),
    path('signup/', views.signup, name='sugnup'),
    path('signup/signup_ok', views.signup_ok, name = 'signup_ok'),
    path('board/', views.board_page, name='board'),
    path('page2/', views.ad_page, name='page2'),
    path('login/', views.login, name='login'),
    path('login/login_ok/', views.login_ok, name='login_ok'),
    path('logout', views.logout, name='logout'),
    path('notice/', views.notice, name='notice'),
    path('notice/content/<int:id>', views.content, name='content'),
    path('notice/search/', views.search, name='search'),
    path('search_page/', views.search_page, name='search_page'),
    path('search_subpage/', views.search_subpage, name='search_subpage'),
    path('board/write/', views.write_page, name='write'), 
    path('login/forgot_password/', views.forgot_password, name='forgot_password'),
    path('login/forgot_password/forgot_password_ok/', views.forgot_password_ok, name='forgot_password_ok'),
    path('login/forgot_password/forgot_password_ok/', views.forgot_password_ok, name='forgot_password_ok'),
    path('mypage', views.mypage, name='mypage'),
    path('updateinfo', views.updateinfo, name='updateinfo'),
    path('updateinfo/updateinfo_ok/', views.updateinfo_ok, name='updateinfo_ok'),
    path('deleteAcount', views.deleteAcount, name='deleteAcount'),
    path('deleteAcount/deleteAcount_ok/', views.deleteAcount_ok, name='deleteAcount_ok'),
    path('checkpassword', views.checkpassword, name='checkpassword'),
    path('checkpassword/checkpassword_ok/', views.checkpassword_ok, name='checkpassword'),
    path('resetpassword', views.resetpassword, name='resetpassword'),
    path('resetpassword/resetpassword_ok/', views.resetpassword_ok, name='resetpassword_ok'),
    
    
    
]