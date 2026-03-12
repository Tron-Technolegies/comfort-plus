from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_users(request):
    signup_users = User.objects.all()
    users = []

    for user in signup_users:
        users.append({
            'Name': user.username,
            'Eamil': user.email,
        })
    return JsonResponse(users)