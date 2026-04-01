from urllib import request

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from UserApp.models import  Profile,Service_Booking,Message
from rest_framework.decorators import permission_classes,api_view
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate,login
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.exceptions import ObjectDoesNotExist
from AdminApp.models import Services

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


@csrf_exempt
def user_login(request):
    if request.method == "POST":

        email = request.POST.get("mail")
        password = request.POST.get("pass")

        if not email or not password:
            return JsonResponse({"message": "Email and password required"})

        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            return JsonResponse({"message": "Invalid credentials"})

        user = authenticate(username=user_obj.username, password=password)

        if user is None:
            return JsonResponse({"message": "Invalid credentials"})

        # session login
        login(request, user)

        # JWT tokens
        refresh = RefreshToken.for_user(user)

        return JsonResponse({
            "message": "Login successful",
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email
            }
        })

    return JsonResponse({"message": "Invalid request"})




#*****************************PROFILE*******************************

#VIEW PROFILE

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_profile(request):
    user = request.user
    try:
        profile = user.profile
        phone = profile.Phone
    except ObjectDoesNotExist:
        phone = None

    data = {
        "name": user.username,
        "mail": user.email,
        "phone": phone
    }

    return JsonResponse(data)

#UPDATE PROFILE

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    user = request.user

    # Ensure profile exists
    try:
        profile = user.profile
    except ObjectDoesNotExist:
    
        profile = Profile.objects.create(user=user)

    
    user.username = request.data.get("name", user.username)

    new_email = request.data.get("email", user.email)
    if User.objects.filter(email=new_email).exclude(id=user.id).exists():
        return JsonResponse({"message": "Email already exists"}, status=400)
    user.email = new_email
    user.save()

   
    profile.Phone = request.data.get("phone", profile.Phone)
    profile.save()

    return JsonResponse({"message": "Updated successfully"})





#****************************SERVICE****************************

#*VIEW_SERVICES

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_services(request):
    services = Services.objects.all()
    new_list = []

    for i in services:
        new_list.append({
            "id": i.id,
            "s_nme": i.service_type,
            "disc": i.description,
            "price": i.price,
            "estimated_t": i.estimated_time,
            "is_avail": i.is_available,
            "cr_at": i.created_at,
            "up_st": i.updated_at
        })
    return JsonResponse(new_list, safe=False)

#VIEW_SINGLE_SERVICE

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_single_service(request,id):
    service = Services.objects.get(id=id)

    data = {
        "id": service.id,
        "s_nme": service.service_type,
        "disc": service.description,
        "price": service.price,
        "estimated_t": service.estimated_time,
        "is_avail": service.is_available,
        "cr_at": service.created_at,
        "up_st": service.updated_at
    }

    return JsonResponse(data)

#*************************SCHEDEULE*****************************

#SERVICE_BOOKING

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def place_order(request):

    rfull_name = request.data.get("full_name")
    rphone = request.data.get("phone")
    rmail = request.data.get("email")
    raddress = request.data.get("street_address")
    rcity = request.data.get("city")
    rzipcode = request.data.get("zipcode")
    rservice_type = request.data.get("service")
    rdate = request.data.get("date")
    rtime = request.data.get("time")
    rdelivery_mode = request.data.get("delivery_mode")

    Service_Booking.objects.create(
        user=request.user,
        full_name=rfull_name,
        phone=rphone,
        email=rmail,
        street_address=raddress,
        city=rcity,
        zipcode=rzipcode,
        service=rservice_type,
        date=rdate,
        time=rtime,
        Delivery_mode=rdelivery_mode
    )

    return JsonResponse({"message": "Success"})

    
#VIEW_ORDER

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_order(request):
        schedule=Service_Booking.objects.filter(user=request.user)
        data=[]
        for i in schedule:
            data.append(
                {
                    "full_name":i.full_name,
                    "phone":i.phone,
                    "email":i.email,
                    "street_address":i.street_address,
                    "city":i.city,
                    "zipcode":i.zipcode,
                    "service":i.service,
                    "date":i.date,
                    "time":i.time
                }
            )
        return JsonResponse(data,safe=False)

#******************MESSAGE***************

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_message(request):

    rmail=request.POST.get("mail")
    rsubject=request.POST.get("subject")
    rmessage=request.POST.get("message")
    if not rmail:
        return HttpResponse("This is mandatory")
    Message.objects.create(
        user=request.user,
        email=rmail,
        subject=rsubject,
        message=rmessage
    )
    return HttpResponse("Success")

#RESET_PASSWORD

# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def reset_password(request):

#     password=request.data.get("current password")
#     new_password=request.data.get("new_password")
#     confirm_password=request.data.get("confirm_password")
#     user = request.user
#     if not User.check_password(password):
#      return HttpResponse("Incorrect password")
#     if new_password != confirm_password:
#        return HttpResponse("Passwords do not match")
# # set new password
#     user.set_password(new_password)
#     user.save()
    # return JsonResponse({"message":"success"})

