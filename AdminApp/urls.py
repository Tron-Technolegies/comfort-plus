from django.urls import path
from AdminApp import views

urlpatterns= [
    path('view_users/', views.view_users, name='view_users'),

    path('add_service/', views.add_service, name='add_service'),
    path('view_services/', views.view_services, name='view_services'),
    path('v_single_services/<int:id>', views.v_single_services, name='v_single_services'),
    path('edit_service/<int:id>', views.edit_service, name='edit_service'),
    path('delete_service/<int:id>', views.delete_service, name='delete_service'),

]