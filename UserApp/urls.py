from django.urls import path
from UserApp import views

urlpatterns = [
    path("signup/", views.user_signup, name="user_signup"),
]