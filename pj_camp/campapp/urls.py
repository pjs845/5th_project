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
    path('logout/', views.logout, name='logout'),
    path('notice/', views.notice, name='notice'),
    path('notice/content/<int:id>', views.content, name='content'),
    path('notice/search/', views.search, name='search'),
    path('search_page/', views.search_page, name='search_page'),
    path('search_subpage/', views.search_subpage, name='search_subpage'),
    path('board/write/', views.write_page, name='write'), 
    path('download/<int:pk>', views.notice_download_view, name="notice_download"),

]

from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)