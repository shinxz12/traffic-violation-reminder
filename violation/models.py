from django.db import models

# Create your models here.


class Vehicle(models.Model):
    TYPES = [("CAR", "CAR"), ("MOTO_BIKE", "MOTO_BIKE"), ("ELECTRIC_BIKE", "ELECTRIC_BIKE")]
    type = models.CharField(choices=TYPES, max_length=32)
    number_plate = models.CharField(max_length=32, unique=True)
    email = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=32, null=True, blank=True)
