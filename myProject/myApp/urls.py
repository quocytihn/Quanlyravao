from django.urls import path
from . import views


urlpatterns = [
    #url login
    path('',views.cv_view2,name ='cv2'),
    path('cv/',views.cv_view_pro,name ='cv'),
]