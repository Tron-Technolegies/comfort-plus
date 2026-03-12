from django.db import models


class Services(models.Model):
    service_type = models.CharField(max_length=100)
    description = models.TextField(blank=True)