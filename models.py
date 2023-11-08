from django.db import models
from django.contrib.auth.models import User 


# Create your models here.

class Address(models.Model):
    home_address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)

class Userdetails(models.Model):
    full_name = models.CharField(max_length=50 , null=True)
    email = models.EmailField(max_length=50 , null=True)
    phone = models.CharField(max_length=50 , null=True)
    username = models.CharField(max_length=10)
    password = models.CharField(max_length=6)
    address = models.OneToOneField(Address, on_delete=models.CASCADE, null=True, blank=True)



class Service(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=500)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=False)

class Technician(models.Model):
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=100)
    specialization = models.CharField(max_length=255)
    is_staff = models.BooleanField(default=True)  # Add the is_staff field

    def __str__(self):
        return self.username



class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    service_type = models.CharField(max_length=100)
    laptop_brand = models.CharField(max_length=100, blank=True, null=True)
    laptop_model = models.CharField(max_length=100, blank=True, null=True)
    service_description = models.TextField()
    service_cost = models.DecimalField(max_digits=10, decimal_places=2)
    booking_date = models.DateField()
    booking_time = models.CharField(max_length=20)

    def __str__(self):
        return f'Booking for {self.full_name}'




