from django.urls import path
from . import views
from . import upload_images

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('questions/', views.question_list, name='question_list'),
    path('ask/', views.ask_question, name='ask_question'), 
    path('question/<int:question_id>/answer/', views.answer_question, name='answer_question'),
    path('delete_question/<int:question_id>/', views.delete_question, name='delete_question'),

    # 图片上传验证
    path('index/', upload_images.index, name='index'),
    path('verify/', upload_images.verify_answer, name='verify_answer'),
    path('upload/', upload_images.upload_image, name='upload_image'),
    path('images/', upload_images.image_list, name='image_list'),
    path('upload_images/', upload_images.upload_images, name='upload_images'),
    path('upload_page/',upload_images.upload_page, name='upload_page'),
    path('delete_image/<int:image_id>/', upload_images.delete_image, name='delete_image'),
    path('deal/', views.deal_cards, name='deal_cards'),
    path('game/', views.game_page, name='game_page'),

]
