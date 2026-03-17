from urllib import request
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User

from AdminApp.models import Services


@api_view(["POST"])
def add_service(request):
    service_nme = request.POST.get("s_name")
    disc = request.POST.get("discription")
    s_price = request.POST.get("s_prc")
    estimated_t = request.POST.get("est_time")
    available = request.POST.get("is_available") == "True"
    created_at = request.POST.get("created_at")
    updated_at = request.POST.get("updated_at")

    if not service_nme or not s_price:
        return HttpResponse("its a mandatory field", status=400)

    try:
        Services.objects.create(
            service_type=service_nme,
            description=disc,
            price=s_price,
            estimated_time=estimated_t,
            is_available=available,
            created_at=created_at,
            updated_at=updated_at,
        )
        return HttpResponse("create successfully", status=201)
    except Exception as e:
        return HttpResponse(str(e), status=500)


@api_view(['GET'])
def view_services(request):
    services = Services.objects.all()
    new_list = []

    for i in services:
        new_list.append({
            "id": i.id,
            "s_nme": i.service_type,
            "disc": i.description,
            "pr": i.price,
            "estimated_t": i.estimated_time,
            "is_avail": i.is_available,
            "cr_at": i.created_at,
            "up_st": i.updated_at
        })
    return JsonResponse(new_list, safe=False)

@api_view(['GET'])
def v_single_services(request,id):
    data =  get_object_or_404(Services,id=id)
    service = {
                "id": data.id,
                "s_nme": data.service_type,
                "disc": data.description,
                "pr": data.price,
                "estimated_t": data.estimated_time,
                "is_avail": data.is_available,
                "cr_at": data.created_at,
                "up_st": data.updated_at
              }
    return JsonResponse(service)

@csrf_exempt
def edit_service(request,id):
    if request.method == 'GET':
        s_data = Services.objects.get(id=id)
        single_data = {
            "id": s_data.id,
            "s_nme": s_data.service_type,
            "disc": s_data.description,
            "pr": s_data.price,
            "estimated_t": s_data.estimated_time,
            "is_avail": s_data.is_available,
            "cr_at": s_data.created_at,
            "up_st": s_data.updated_at
        }
        return JsonResponse(single_data)
    
    elif request.method == 'POST':
        s_data = Services.objects.get(id=id)
        s_data.service_type = request.POST.get('s_nme', )
        s_data.description = request.POST.get('disc', s_data.description)
        s_data.price = request.POST.get('s_pr', s_data.price)
        s_data.estimated_time = request.POST.get('est_t', s_data.estimated_time)
        s_data.is_available = request.POST.get('is_avl', s_data.is_available)
        s_data.updated_at = request.POST.get('up_at', s_data.updated_at)
        s_data.save()
        return HttpResponse("updated successfully",status=201)
    
    return JsonResponse("completed")

@api_view(['DELETE'])
def delete_service(request,id):
        data = Services.objects.get(id=id)
        data.delete()
        return JsonResponse({'message':'successfully deleted'})

# .....................view user..........................
@api_view(["GET"])
def view_users(request):
    signup_users = User.objects.all()
    users = []

    for user in signup_users:
        users.append(
            {
                "Name": user.username,
                "Email": user.email,
            }
        )
    return JsonResponse(users, safe=False)
