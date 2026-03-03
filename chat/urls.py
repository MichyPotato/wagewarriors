from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='chat.index'),
    path('<str:user1_username>/<str:user2_username>/', views.chat_room, name='chat.room'),
]