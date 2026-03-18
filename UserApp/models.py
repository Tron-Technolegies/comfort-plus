from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.


class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    Phone=models.IntegerField()

class Service_Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    street_address = models.TextField()
    city = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=10)
    service = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    Delivery_mode = models.CharField(max_length=10,choices=[('Normal', 'Normal'),('Express', 'Express')],default='null')#→ value stored in the database→ value shown in forms
    order_id=models.UUIDField(default=uuid.uuid4,editable=False,unique=True)


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()

