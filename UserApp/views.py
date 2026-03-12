from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from UserApp.models import  Profile

# Create your views here.

@csrf_exempt
def user_signup(request):
    if request.method=='POST':
        rname=request.POST.get("name")
        rmail=request.POST.get("mail")
        rphone=request.POST.get("phone")
        rpass=request.POST.get("pass")
        if not rmail or not rphone:
            return HttpResponse("This field is mandatory")
        user=User.objects.create_user(
            username=rname,
            email=rmail, 
            password=rpass
        )
        Profile.objects.create(
            user=user,
            Phone=rphone
        )
    return JsonResponse({'message':'successfully'})