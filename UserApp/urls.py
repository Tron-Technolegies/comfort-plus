from django.urls import path
from UserApp import views

urlpatterns = [
    
    path("signup/", views.user_signup, name="user_signup"),

    path("view_profile",views.view_profile,name="view_profile"),
    path("update_profile",views.update_profile,name="update_profile"),
    path("delete_profile",views.delete_profile,name="delete_profile"),
]