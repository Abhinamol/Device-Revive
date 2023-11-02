from django.db import models



# Create your models here.

class Userdetails(models.Model):
    full_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=50)
    username = models.CharField(max_length=10)
    password = models.CharField(max_length=6)




class Service(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=500)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=False)

class Technician(models.Model):
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)  # You can adjust the max length as needed
    email = models.EmailField()
    username = models.CharField(max_length=50, unique=True)  # Assuming you want usernames to be unique
    password = models.CharField(max_length=100)
    specialization = models.CharField(max_length=255)