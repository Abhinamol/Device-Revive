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
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    address_choice = models.CharField(max_length=20)
    address = models.ForeignKey(
        Address,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    ) 
    new_home_address = models.TextField(blank=False, null=False)
    new_city = models.CharField(max_length=100, blank=False, null=False)
    new_pincode = models.CharField(max_length=10,blank=False, null=False)
    service_type = models.CharField(max_length=20)
    laptop_brand = models.CharField(max_length=20, blank=False, null=False)
    laptop_model = models.CharField(max_length=50, blank=False, null=False)
    selected_services = models.TextField()
    service_mode = models.CharField(max_length=20)
    onsite_service_charge = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    total_service_cost = models.DecimalField(max_digits=10, decimal_places=2)
    from_date = models.DateField()
    selected_slot = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.full_name} - {self.from_date}"




