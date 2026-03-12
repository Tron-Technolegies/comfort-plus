from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
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
