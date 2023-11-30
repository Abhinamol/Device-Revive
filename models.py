from django.db import models
from django.contrib.auth.models import User 


# Create your models here.

class Address(models.Model):
    home_address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)

class Userdetails(models.Model):
    full_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=50)
    username = models.CharField(max_length=10)
    password = models.CharField(max_length=6)
    address = models.OneToOneField(Address, on_delete=models.CASCADE, null=True, blank=True)



class Service(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=500)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=False)


class LaptopBrand(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Technician(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True,blank=True)
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=100)
    is_staff = models.BooleanField(default=True)  # Add the is_staff field
    address = models.ForeignKey(Address, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.username


class Booking(models.Model):
    device_type_choices = [
        ('laptop', 'Laptop'),
        ('desktop', 'Desktop'),
    ]

    device_type = models.CharField(max_length=7, choices=device_type_choices)
    brand = models.CharField(max_length=50, null=True, blank=True)
    model = models.CharField(max_length=50, null=True, blank=True)
    preferred_date = models.DateField(null=False, blank=False)
    preferred_time = models.TimeField(null=False, blank=False)
    selected_services = models.ManyToManyField(Service, blank=True)
    total_service_cost = models.DecimalField(max_digits=10, decimal_places=2)


    def __str__(self):
        return f"{self.device_type} - {self.brand} - {self.model}"




