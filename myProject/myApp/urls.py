from django.urls import path
from . import views


urlpatterns = [
    #url login
    path('',views.cv_view2,name ='cv2'),
    #path('',views.cv_view,name ='cv'),
    path('login/', views.login_view, name='login'),
    #url home
    path('home/', views.home_view, name='home'),
    path('register/', views.register_view, name='register'), 
    path('thongbao/', views.Notification, name='thongbao'), 
    #url admin
    path('waiting_list/', views.waiting_list, name='waiting'),
    path('diary_form/',views.diary_form,name='diary_form'),
    path('diary_list/',views.diary_list,name='diary_list'),
    #url logout
    path('logout/', views.logout_view, name='logout'),
]
