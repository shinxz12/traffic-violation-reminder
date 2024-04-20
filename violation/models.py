from django.db import models

# Create your models here.


class Vehicle(models.Model):
    TYPES = [("CAR", "CAR"), ("MOTOBIKE", "MOTOBIKE"), ("ELECTRIC_BIKE", "ELECTRIC_BIKE")]
    type = models.CharField(choices=TYPES, max_length=32)
    number_plate = models.CharField(max_length=32, unique=True)
    email = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=32, null=True, blank=True)
    last_violation = models.DateTimeField(null=True, blank=True)
