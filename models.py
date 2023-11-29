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


class Appointment(models.Model):
    user_details = models.ForeignKey(Userdetails, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)

    service_type = models.CharField(max_length=20, choices=[('Laptop', 'Laptop Service'), ('Desktop', 'Desktop Service')])
    laptop_brand = models.CharField(max_length=20, blank=False, null=False)
    laptop_model = models.CharField(max_length=50,blank=False, null=False )
    selected_services = models.CharField(max_length=255,blank=False, null=False )
    service_mode = models.CharField(max_length=20, choices=[('OnSite', 'On-Site Service'), ('ServiceCenter', 'Service Center')])
    onsite_service_charge = models.DecimalField(max_digits=10, decimal_places=2,blank=False, null=False )
    total_service_cost = models.DecimalField(max_digits=10, decimal_places=2,blank=False, null=False)
    from_date = models.DateField()
    selected_slot = models.CharField(max_length=20)




