from django.urls import path
from AdminApp import views

urlpatterns= [
    path('view_users/', views.view_users, name='view_users'),

    path('add_service/', views.add_service, name='add_service'),

]