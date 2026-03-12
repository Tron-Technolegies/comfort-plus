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
        

        if User.objects.filter(email=rmail).exists():
           return HttpResponse("Email already exists")
        

        user=User.objects.create_user(
            username=rname,
            email=rmail, 
            password=rpass
        )
        Profile.objects.create(
            user=user,
            Phone=rphone
        )
        return JsonResponse({'message': 'successfully created'})

    return JsonResponse({'message': 'invalid request'})


#*****************************PROFILE*******************************

#VIEW PROFILE

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def view_profile(request):
    user=request.user
    profile=user.profile
    phone = profile.phone

    data={
        "name":user.username,
        "mail":user.email,
        "phone":phone
    }

    return JsonResponse(data)

#UPDATE PROFILE

@api_view(['POST'])
@permisiion_classes([IsAuthenticated])
def update_profile(request):
    user=request.user
    profile=user.profile
    user.username=request.data.get("name",user.username)
    user.save()
    new_email = request.data.get("email", user.email)
    if User.objects.filter(email=new_email).exclude(id=user.id).exists():
        return JsonResponse({"message": "Email already exists"})
    
    user.email = new_email
    user.save() 

    profile.phone=request.data.get("phone",profile.phone)
    profile.save()
    return JsonResponse({"message":"Update succesfully"})
    
# @api_view(['DELETE'])
# @permisiion_classes([IsAuthenticated])
# def delete_profile(request):




