from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User




# .....................view user..........................
@api_view(['GET'])
def view_users(request):
    signup_users = User.objects.all()
    users = []

    for user in signup_users:
        users.append({
            'Name': user.username,
            'Email': user.email,
        })
    return JsonResponse(users, safe=False)