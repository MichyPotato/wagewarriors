from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='account.index'),
    path('signup/seeker/', views.seeker_signup, name='account.seeker_signup'),
    path('signup/recruiter/', views.recruiter_signup, name='account.recruiter_signup'),
    path('login/', views.login, name='account.login'),
]