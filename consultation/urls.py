from django.urls import path
from . import views
from . import upload_images

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    # 图片上传验证
    path('index/', upload_images.index, name='index'),
    path('verify/', upload_images.verify_answer, name='verify_answer'),
    path('upload/', upload_images.upload_image, name='upload_image'),
    path('upload_images/', upload_images.upload_images, name='upload_images'),  
    path('delete_image/<int:image_id>/', upload_images.delete_image, name='delete_image'),

]

