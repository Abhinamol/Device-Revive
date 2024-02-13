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
    address = models.OneToOneField(Address, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.username


class Booking(models.Model):
    device_type_choices = [
        ('laptop', 'Laptop'),
        ('desktop', 'Desktop'),
    ]
    userdetails = models.OneToOneField(Userdetails, on_delete=models.CASCADE, null=True, blank=True)
    device_type = models.CharField(max_length=7, choices=device_type_choices)
    brand = models.CharField(max_length=50, null=True, blank=True)
    preferred_date = models.DateField(null=False, blank=False)
    preferred_time = models.TimeField(null=False, blank=False)
    selected_services = models.ManyToManyField(Service, blank=True)
    total_service_cost = models.DecimalField(max_digits=10, decimal_places=2)
    is_verified = models.BooleanField(default=False)
    razorpay_payment_id = models.CharField(max_length=100, null=True, blank=True)  # Add this field



class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)  # Change here
    payment_date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.BooleanField(default=False)
    razorpay_payment_id = models.CharField(max_length=100, null=True, blank=True)
    razorpay_signature = models.CharField(max_length=200, null=True, blank=True)




class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(max_length=250)
    rating = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)


class SecondHandProduct(models.Model):
    CONDITION_CHOICES = (
        ('new', 'New'),
        ('used', 'Used'),
        ('refurbished', 'Refurbished'),
    )

    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    description = models.TextField()
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES)
    year = models.CharField(max_length=4)  # Assuming year is a string, adjust if necessary
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product_images')
    is_available = models.BooleanField(default=True)  # New field for availability

    def __str__(self):
        return self.name


class ProductExchange(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(SecondHandProduct, on_delete=models.CASCADE)
    exchange_date = models.DateTimeField(auto_now_add=True)
    additional_notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username} exchanged {self.product.name} on {self.exchange_date}"



class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(SecondHandProduct, through='CartItem')

    def __str__(self):
        return f"Cart for {self.user.username}"

class CartItem(models.Model):
    product = models.ForeignKey(SecondHandProduct, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.product.name} in {self.cart.user.username}'s cart"