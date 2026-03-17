from django.urls import path
from UserApp import views

urlpatterns = [
    
    path("signup/", views.user_signup, name="user_signup"),
    path("login/", views.user_login, name="user_login"),

    #*********************PROFILE***********************

    path("view_profile",views.view_profile,name="view_profile"),
    path("update_profile",views.update_profile,name="update_profile"),

    #*********************SERVICES***********************

    path("view_services",views.view_services,name="view_services"),
    path("view_single_service",views.view_single_service,name="view_single_service"),


    #***********************SCHEDULE**************************

    path("place_order",views.place_order,name="place_order"),
    path("view_order",views.view_order,name="view_order"),

#***********************MESSAGE**************************

    path("send_message",views.send_message,name="send_message"),
    
]