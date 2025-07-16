from django.urls import path
from . import views
from . import car
urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),


    path('upload_used_car/', car.upload_used_car, name='upload_used_car'),
    path('car_list/', car.car_list, name='car_list'),
    path('car_list_page/', car.car_list_page, name='car_list_page'),  # 展示页面
    path('dashboard/', views.dashboard, name='dashboard'),

]

