from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth import authenticate,login
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib import auth
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from.models import Userdetails, Address 
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.shortcuts import get_object_or_404
from .forms import ServiceForm
from .models import Service, LaptopBrand
from .models import Technician
from django.contrib.auth.hashers import check_password 
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.urls import reverse
from .models import Booking,Payment
import datetime
from django.db import IntegrityError, transaction
from django.http import Http404
from .models import Review 
from django.contrib.auth import get_user_model
from django.http import HttpResponseForbidden
from .razorpay import generate_order
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import SecondHandProduct, Cart, CartItem
from django.db.models import Q
import json
from .models import Deliveryboy
from django.core.mail import send_mail
from django.conf import settings
from .models import Wishlist, WishlistItem
from .models import Category,Order
from django.http import HttpResponseBadRequest
import random
from django.db.models import Count
from .models import LeaveApplication
from datetime import datetime
from django.db.models import Sum







#create your views here
@never_cache
def index(request):
    reviews = Review.objects.all()  # Fetch all reviews
    return render(request, 'index.html', {'reviews': reviews})



def loginn(request):
    if request.method == "POST":
        username = request.POST['username'].lower()
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            request.session['username'] = user.username

            if username == 'admin' and password == 'admin':
                return redirect('dashboard')  # Redirect admin to the admin page

            # Check if the user is a Technician
            try:
                technician = Technician.objects.get(username=username)
                if technician.password == password:
                    return redirect("booking_details")  # Redirect to staff_profile for Technicians
            except Technician.DoesNotExist:
                pass  # No Technician with this username

            # Check if the user is a DeliveryBoy
            try:
                delivery_boy = Deliveryboy.objects.get(username=username)
                if delivery_boy.password == password:
                    return redirect("deliveryboyprofile")  # Redirect to delivery boy dashboard
            except Deliveryboy.DoesNotExist:
                pass  # No DeliveryBoy with this username

            return redirect('userprofile')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('login')

    response = render(request, "login.html")
    response['Cache-Control'] = 'no-store, must-revalidate'
    return response

    
@never_cache    
def signup(request):
    if request.method == "POST":
       full_name = request.POST['full-name']
       phone_num = request.POST['phone']
       username = request.POST['username']
       email = request.POST['email']
       password = request.POST['password']
       myuser = User.objects.create_user(username,email,password)
       myuser.save()

       user_obj=Userdetails(full_name=full_name,email=email,phone=phone_num,username=username,password=password)
       user_obj.save()
       
       
       return redirect('login')
    return render(request,'reg.html')


def check_username_availability(request):
    username = request.GET.get("username")
    try:
        user = User.objects.get(username=username)
        available = False
    except User.DoesNotExist:
        available = True
    return JsonResponse({"available": available})


def check_email_availability(request):
    email = request.GET.get('email', None)
    data = {}
    if email:
        # Check if the email exists in the database using Django's User model
        if User.objects.filter(email=email).exists():
            data['available'] = False
        else:
            data['available'] = True
    else:
        data['error'] = 'Invalid request'
    return JsonResponse(data)

    
@never_cache 
def dashboard(request):
    return render(request, 'dashboard.html') 

@never_cache 
@login_required(login_url='login')
def servicedetails(request):
    return render(request, 'servicedetails.html') 

@never_cache 
@login_required(login_url='login')
def staffs(request):
    return render(request, 'staffs.html') 


@never_cache 
@login_required(login_url='login')
def userdetailss(request):
    if request.user.is_superuser:
        users = Userdetails.objects.exclude(username='admin')  # Query the custom Userdetails model
        return render(request, "userdetailss.html", {"users": users})
    return redirect("index")


@never_cache 
@login_required(login_url='login')
def dashboard(request):
    if request.user.is_superuser:
        users = Userdetails.objects.exclude(username='admin')  # Query the custom Userdetails model
        return render(request, "dashboard.html", {"users": users})
    return redirect("index")



@never_cache
def services(request):
    return render(request,'services.html')

@never_cache
@login_required(login_url='login')
def userprofile(request):
    if 'username' in request.session:
        response = render(request,"userprofile.html")
        response['Cache-Control'] = 'no-store,must-revalidate'
        return response
    else:
        return redirect('login')

@never_cache
def about(request):
    return render(request,'about.html')

@never_cache
def contact(request):
    return render(request,'contact.html')

@never_cache
@login_required(login_url='login')
def myprofile(request):
    # Assuming you have a Userdetails object associated with the user
    user_details = Userdetails.objects.get(username=request.user.username)

    context = {
        'user_details': user_details,
    }
    return render(request, 'myprofile.html', context)

@never_cache
@login_required(login_url='login')
def staff_profile(request):
    # Get the current user
    user = request.user

    if request.method == 'POST':
        # Update or create the Technician model details
        technician, created = Technician.objects.get_or_create(username=user.username)

        technician.full_name = request.POST.get('fullName', "")
        technician.email = request.POST.get('eMail', "")
        technician.phone_number = request.POST.get('phone', "")
        technician.street = request.POST.get('Street', "")
        technician.city = request.POST.get('ciTy', "")
        technician.state = request.POST.get('sTate', "")
        technician.zip_code = request.POST.get('zIp', "")
        technician.save()

        # Redirect to the profile page after updating
        return render(request, 'staff_profile.html', {'technician_details': technician})

    # Retrieve the technician details
    technician_details = Technician.objects.get(username=user.username)

    return render(request, 'staff_profile.html', {'technician_details': technician_details})

@never_cache
@login_required(login_url='login')
def update(request):
    return render(request,'update.html')

@never_cache
@login_required(login_url='login')
def booking(request):
    services = Service.objects.all()
    return render(request, 'booking.html', {'services': services})



@never_cache
@login_required(login_url='login')
def desktop(request):
    return render(request,'desktop.html')

@never_cache
@login_required(login_url='login')
def staff_services(request):
    services = Service.objects.all()
    return render(request, 'staff_services.html', {'services': services})


 
@never_cache
@login_required(login_url='login')
def bookingconfirmation(request, userid, bookingid):
    try:
        booking = Booking.objects.get(userdetails__id=userid, id=bookingid)
    except Booking.DoesNotExist:
        return HttpResponse("Booking does not exist for this user or it has already been verified")

    
    payment_amount = booking.total_service_cost * 100

    context = {
        'selected_services': booking.selected_services.all(),
        'total_cost': booking.total_service_cost,
        'selected_date': booking.preferred_date,
        'selected_time': booking.preferred_time,
        'userid': userid,
        'bookingid': bookingid,
        'payment_amount': payment_amount  
    }
    return render(request, 'bookingconfirmation.html', context)



@never_cache
def why(request):
    return render(request,'why.html')

def after_login(request):
    return render(request,'after_login.html')

@never_cache
def logout (request):
    auth.logout(request)
    return redirect('/')

def handlelogout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('login')


@never_cache
@login_required
def userprofile(request):
    # Get the user's name
    username = request.user.username

    # Pass the user's name to the template
    return render(request, 'userprofile.html', {'username': username})

def delete_user(request, user_id):
    user = get_object_or_404(Userdetails, pk=user_id)
    user.delete()
    return HttpResponse('User deleted successfully')

@never_cache
@login_required(login_url='login')
def servicedetails(request):
    services = Service.objects.all()
    return render(request, 'servicedetails.html', {'services': services})




@never_cache
@login_required(login_url='login')
def add_service(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new service to the database
            return redirect('servicedetails')  # Redirect to a service list page

    # If the form is not valid or it's a GET request, render the form page
    else:
        form = ServiceForm()

    return render(request, 'add_service.html', {'form': form})


def delete_service(request, service_id):
    # Get the service instance to delete
    service = get_object_or_404(Service, pk=service_id)

    # Delete the service
    service.delete()

    return redirect('servicedetails') 

@never_cache
@login_required
def edit_service(request, service_id):
    service = Service.objects.get(id=service_id)

    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            return redirect('servicedetails')

    else:
        form = ServiceForm(instance=service)

    return render(request, 'edit_service.html', {'form': form, 'service': service})


@never_cache
@login_required
def update_service(request, service_id):
    # Your view logic here
    service = Service.objects.get(pk=service_id)

    if request.method == "POST":
        # Process and update the service data here
        # ...

        return redirect('edit_service')  # Redirect to the edit service page

    return render(request, 'update_service.html', {'service': service})


@never_cache
@login_required(login_url='login')
def updateuser(request):
    if request.method == 'POST':
        # Get or create Userdetails object
        user_details, created = Userdetails.objects.get_or_create(username=request.user.username)

        # Get form data
        full_name = request.POST.get('full-name')
        email = request.POST.get('eMail')
        phone = request.POST.get('phone')
        username = request.POST.get('username')
        home_address = request.POST.get('home')
        city = request.POST.get('city')
        pincode = request.POST.get('zip')

        # Check if email is not empty before saving
        if email:
            user_details.email = email
        user_details.phone = phone
        user_details.username = username
        user_details.save()

        # Check if home_address is not empty before saving
        if home_address:
            if user_details.address:
                address = user_details.address
            else:
                address = Address()

            address.home_address = home_address
            address.city = city
            address.pincode = pincode
            address.save()

            # Update user_details.address with the newly created or existing Address object
            user_details.address = address

        user_details.save()

        # Redirect to the profile page
        return redirect('myprofile')

    # Assuming you have a Userdetails object associated with the user
    user_details, created = Userdetails.objects.get_or_create(username=request.user.username)

    context = {
        'user_details': user_details,
    }
    return render(request, 'updateuser.html', context)


@never_cache
@login_required
def book_now(request, service_id):
    return redirect('booknow')


@never_cache
@login_required
def add_staff(request):
    if request.method == "POST":
        # Get the form data
        full_name = request.POST.get('full_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')  # Add this line to get the email field

        # Perform validation checks here (e.g., checking for required fields, unique usernames, etc.)
        errors = {}
        if not full_name:
            errors['full_name'] = 'Full Name is required'
        if not username:
            errors['username'] = 'Username is required'
        # Add more validation checks as needed

        if errors:
            return render(request, 'add_staff.html', {'errors': errors})

        # Create a new Technician object and save it to the database
        technician = Technician(
            full_name=full_name,
            username=username,
            password=password,
            email=email,
        )
        technician.save()

        # Create a new User object and save it to the database for authentication
        user = User.objects.create_user(username=username, password=password, email=email)  # Add email field
        user.is_staff = True
        user.save()

        send_mail(
            'Welcome to Your Site',
            f'Dear {full_name},\n\nYou have been added as a staff member. Your username is {username} and password is {password}. '
             f'Please log in with these credentials..'
              f'Remember to update your profile and change the temporary password provided.\n\n' \
              f'Thank you!\nDevice Revive',
            'your_email@example.com',  # Replace with your email address
            [email],  # Use the staff member's email address
            fail_silently=False,
        )

        # Redirect to a different page after adding the technician
        return redirect('staffs')  # Redirect to the technician list view

    return render(request, 'add_staff.html')

@never_cache
@login_required
def staffs(request):
    staff_data = Technician.objects.all()  # Fetch all staff data from the database

    # Print staff details for debugging
    for staff in staff_data:
        print(staff.id, staff.full_name, staff.email, staff.phone_number, staff.username)

    context = {
        'staff_data': staff_data,
    }

    return render(request, 'staffs.html', context)



def delete_staff(request, staff_id):
    if request.method == 'POST':
        # Get the technician object
        technician = Technician.objects.get(pk=staff_id)
        # Update the is_available status
        technician.is_available = not technician.is_available
        technician.save()
    # Redirect back to the staff details page
    return redirect('staffs')


@csrf_exempt
def check_username_availability(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        
        # Check if the username already exists
        user_exists = User.objects.filter(username=username).exists()
        
        return JsonResponse({'usernameExists': user_exists})
    
    return JsonResponse({'error': 'Invalid request method'})



@never_cache
@login_required
def staff_update(request):
    # Try to get the associated Technician object or create a new one
    technician, created = Technician.objects.get_or_create(user=request.user)

    if request.method == "POST":
        technician.full_name = request.POST.get("full_name", "")
        technician.email = request.POST.get("email", "")
        technician.phone_number = request.POST.get("phone", "")
        technician.username = request.POST.get("username", "")
        technician.save()

        if not technician.address:
            address = Address()
        else:
            address = technician.address

        address.home_address = request.POST.get("home", "")
        address.city = request.POST.get("city", "")
        address.pincode = request.POST.get("zip", "")
        address.save()

        # Update technician.address with the newly created or existing Address object
        technician.address = address
        technician.save()

    return render(request, "staff_update.html", {'technician': technician})




@never_cache
@login_required(login_url='login')
def booknow(request):
    total_cost = 0

    if request.method == 'POST':
        # Extract form data from the request
        device_type = request.POST.get('deviceType')
        brand = request.POST.get('brand')
        model = request.POST.get('model')
        preferred_date = request.POST.get('preferredDate')
        preferred_time = request.POST.get('preferredTime')
        selected_services = request.POST.getlist('selected_services')
        total_cost = sum(float(service.price) for service in Service.objects.filter(id__in=selected_services))

        # Retrieve the Userdetails instance for the logged-in user
        user_details = Userdetails.objects.get(username=request.user.username)

        # Check if a Booking instance already exists for the Userdetails
        try:
            with transaction.atomic():
                booking_instance = Booking.objects.select_for_update().get(userdetails=user_details)
                # If it exists, update the existing Booking instance
                booking_instance.device_type = device_type
                booking_instance.brand = brand
                booking_instance.preferred_date = preferred_date
                booking_instance.preferred_time = preferred_time
                booking_instance.total_service_cost = total_cost
                booking_instance.save()
                # Update selected services in the ManyToManyField
                booking_instance.selected_services.set(selected_services)
        except Booking.DoesNotExist:
            # If it doesn't exist, create a new Booking instance
            booking_instance = Booking(
                userdetails=user_details,
                device_type=device_type,
                brand=brand,
                preferred_date=preferred_date,
                preferred_time=preferred_time,
                total_service_cost=total_cost,
            )
            booking_instance.save()
            # Add selected services to the ManyToManyField
            booking_instance.selected_services.set(selected_services)
        except IntegrityError:
            # Handle IntegrityError, for example, log an error or return an error response
            pass

        return redirect('bookingconfirmation', userid=user_details.id, bookingid=booking_instance.id)

    # Provide choices for laptop brands
    laptop_brand_choices = [
        ('Acer', 'Acer'),
        ('Asus', 'Asus'),
        ('Dell', 'Dell'),
        ('HP', 'HP'),
        ('Lenovo', 'Lenovo'),
        ('Other', 'Other'),
    ]

    # Retrieve services from the Service model
    services = Service.objects.all()

    # Retrieve the Userdetails instance for the logged-in user
    user_details = Userdetails.objects.get(username=request.user.username)

    context = {
        'user_details': user_details,
        'laptop_brand_choices': laptop_brand_choices,
        'services': services,
        'total_cost': total_cost,
    }

    return render(request, 'booknow.html', context)




@csrf_exempt
def check_service_name(request):
    if request.method == 'GET':
        service_name = request.GET.get('name', '')
        service_exists = Service.objects.filter(name__iexact=service_name).exists()
        return JsonResponse({'exists': service_exists})



@never_cache
@login_required(login_url='login')
def booking_details(request):
    if request.method == 'POST':
        booking_id = request.POST.get('booking_id')
        try:
            booking = Booking.objects.get(pk=booking_id)
            user_email = booking.userdetails.email

            # Confirm the booking (you can implement your own logic here)

            # Send confirmation email to the user
            subject = 'Booking Confirmation'
            message = 'Your booking is confirmed.'
            html_message = render_to_string('booking_confirmation_email.html', {'booking': booking})
            plain_message = strip_tags(html_message)

            send_mail(subject, plain_message, 'your_email@example.com', [user_email], html_message=html_message)

            return redirect('booking_details')
        except Booking.DoesNotExist:
            return HttpResponse("Booking not found.")
    
    # Retrieve all booking instances with related Userdetails
    bookings = Booking.objects.select_related('userdetails').all()

    context = {'bookings': bookings}
    return render(request, 'booking_details.html', context)



@login_required(login_url='login')
def confirm_booking(request):
    if request.method == 'POST':
        booking_id = request.POST.get('booking_id')
        try:
            booking = Booking.objects.get(pk=booking_id)

            # Confirm the booking (you can implement your own logic here)

            # Update the is_verified field
            booking.is_verified = True
            booking.save()

            # Send confirmation email to the user
            subject = 'Booking Confirmation'
            message = 'Your booking is confirmed.'
            html_message = render_to_string('booking_confirmation_email.html', {'booking': booking})
            plain_message = strip_tags(html_message)

            send_mail(subject, plain_message, 'your_email@example.com', [booking.userdetails.email], html_message=html_message)

            return redirect('booking_details')
        except Booking.DoesNotExist:
            return JsonResponse({'error': 'Booking not found.'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)


@login_required(login_url='login')
def Review_rate(request):
    if request.method == 'POST':
        comment = request.POST.get('comment')
        rating = request.POST.get('rating')

        # Get the user instance
        try:
            user = get_user_model().objects.get(pk=request.user.pk)
        except get_user_model().DoesNotExist:
            # Handle the case where the user does not exist
            return HttpResponseForbidden("User not found")

        # Create a new review
        review = Review(user=user, comment=comment, rating=rating)
        review.save()

        messages.success(request, 'Review submitted successfully!')
        return redirect('userprofile')
    else:
        return HttpResponseForbidden("Invalid request method")


@login_required
def payment(request, booking_id=None):
    if booking_id:
        booking = get_object_or_404(Booking, id=booking_id)

        if booking.payment_set.exists():
            messages.error(request, "Payment for this appointment is already complete.")
            return redirect("index")

        try:
            order_id = generate_order(booking.total_service_cost)
            if order_id:
                booking.razorpay_order_id = order_id
                booking.save()

                # Get the actual payment ID from Razorpay API response
                # IMPORTANT: Replace "get_this_from_razorpay_response" with the actual payment ID from Razorpay.
                actual_payment_id = "razorpay_payment_id"  # Replace with the actual payment ID

                # Now, you can set the razorpay_payment_id for the booking
                booking.razorpay_payment_id = actual_payment_id
                booking.save()

                context = {
                    "booking": booking,
                    "razorpay_key_id": settings.RAZORPAY_KEY_ID,
                    "order_id": order_id,
                    "callback_url": request.build_absolute_uri(reverse('verify_payment')),
                }
                return render(request, "verify_payment.html", context)
            else:
                messages.error(request, "Error generating order.")
                return redirect("index")

        except Exception as e:
            messages.error(request, f"Error generating order: {str(e)}")
            return redirect("booknow", booking_id=booking_id)

    else:
        try:
            # Fetch the user's cart
            user_cart = Cart.objects.get(user=request.user)
            
            # Calculate the total amount from the cart items
            total_amount = 0
            cart_items = CartItem.objects.filter(cart=user_cart)
            for cart_item in cart_items:
                total_amount += cart_item.product.price * cart_item.quantity

            # Generate order for cart total amount
            order_id = generate_order(total_amount)
            if order_id:
                context = {
                    "cart_items": cart_items,
                    "total_amount": total_amount,
                    "razorpay_key_id": settings.RAZORPAY_KEY_ID,
                    "order_id": order_id,
                    "callback_url": request.build_absolute_uri(reverse('verify_payment')),
                }
                return render(request, "verify_payment.html", context)
            else:
                messages.error(request, "Error generating order.")
                return redirect("index")

        except Cart.DoesNotExist:
            messages.error(request, "Cart not found for this user.")
            return redirect("index")


@csrf_exempt
def verify_payment(request):
    if request.method == "POST":


        try:
            data = json.loads(raw_data)
            order_id = data.get("razorpay_order_id")
            payment_id = data.get("razorpay_payment_id")
            signature = data.get("razorpay_signature")
        except json.JSONDecodeError:
            # If JSON decoding fails, treat it as form-encoded data
            data = request.POST
            order_id = data.get("razorpay_order_id")
            payment_id = data.get("razorpay_payment_id")
            signature = data.get("razorpay_signature")

        if not order_id or not payment_id or not signature:
            messages.error(request, "Invalid request.")
            return redirect("index")

        try:
            booking = Booking.objects.get(razorpay_order_id=order_id)

            # Save Payment instance
            payment = Payment.objects.create(
                user=booking.user,
                booking=booking,
                amount=booking.total_service_cost,
                status=True,
                razorpay_payment_id=payment_id,
                razorpay_signature=signature,
            )

            print(f"Payment saved: {payment}")

            # Perform any additional actions here if needed

            # Render a response (you can customize this based on your needs)
            return render(request, "payment_success.html", {"payment": payment})

        except Booking.DoesNotExist:
            messages.error(request, "Booking not found.")
            return HttpResponse(status=404)
        
        except Exception as e:
            messages.error(request, f"Error processing payment: {str(e)}")
            return HttpResponse(status=500)

    return HttpResponse("Invalid request method.")


@login_required
def payment_success(request):
    if request.method == 'POST':
        # Get the data from the POST request
        userid = request.POST.get('userid')
        bookingid = request.POST.get('bookingid')
        cartid = request.POST.get('cartid')

        # Initialize objects for booking and cart
        booking = None
        cart = None

        # Handle the case of a booking
        if bookingid:
            try:
                # Fetch the booking associated with the provided booking ID
                booking = Booking.objects.get(id=bookingid)
            except Booking.DoesNotExist:
                return HttpResponse("Booking does not exist or it has already been verified")

        # Handle the case of a cart
        if cartid:
            try:
                # Fetch the cart associated with the provided cart ID
                cart = Cart.objects.get(id=cartid)
            except Cart.DoesNotExist:
                return HttpResponse("Cart does not exist")

        # Ensure either booking or cart exists
        if not (booking or cart):
            return HttpResponse("Booking or Cart ID is missing")

        try:
            if booking:
                # Fetch the Userdetails object for a booking
                userdetails = Userdetails.objects.get(id=userid)

                # Create a Payment object for booking
                payment = Payment.objects.create(
                    user=userdetails,
                    booking=booking,
                    amount=booking.total_service_cost,
                    status=True
                )

                # Update the booking details after successful payment
                booking.is_verified = True
                booking.save()

            elif cart:
                # Fetch the Userdetails object for a cart
                userdetails = Userdetails.objects.get(id=userid)

                # Calculate the total amount of cart items
                total_amount = 0
                cart_items = CartItem.objects.filter(cart=cart)
                for cart_item in cart_items:
                    total_amount += cart_item.product.price * cart_item.quantity

                # Create a Payment object for cart
                payment = Payment.objects.create(
                    user=userdetails,
                    amount=total_amount,
                    status=True
                )

                # Clear the cart after successful payment
                cart.products.clear()

            messages.success(request, 'Payment successful!')
            return render(request, 'index.html')

        except Userdetails.DoesNotExist:
            return HttpResponse("Userdetails not found")

    else:
        return render(request, 'index.html')



@never_cache 
@login_required(login_url='login')
def admin_booking(request):
    if request.method == 'POST':
        booking_id = request.POST.get('booking_id')
        try:
            booking = Booking.objects.get(pk=booking_id)
            user_email = booking.userdetails.email

            # Confirm the booking (you can implement your own logic here)

            # Send confirmation email to the user
            subject = 'Booking Confirmation'
            message = 'Your booking is confirmed.'
            html_message = render_to_string('booking_confirmation_email.html', {'booking': booking})
            plain_message = strip_tags(html_message)

            send_mail(subject, plain_message, 'your_email@example.com', [user_email], html_message=html_message)

            return redirect('admin_booking')
        except Booking.DoesNotExist:
            return HttpResponse("Booking not found.")
    
    # Retrieve all booking instances with related Userdetails
    bookings = Booking.objects.select_related('userdetails').all()

    context = {'bookings': bookings}
    return render(request, 'admin_booking.html', context)

    
@never_cache
@login_required(login_url='login')
def add_second_hand_product(request):
    if request.method == 'POST':
        brand = request.POST.get('brand')
        model = request.POST.get('model')
        description = request.POST.get('description')
        condition = request.POST.get('condition')
        year = request.POST.get('year')
        price = request.POST.get('price')
        image = request.FILES.get('image')
        added_by = Userdetails.objects.get(username=request.user.username)
        category_id = request.POST.get('category')  # Retrieve the selected category ID from the form data

        # Create the SecondHandProduct object
        product = SecondHandProduct.objects.create(
            added_by=added_by,
            brand=brand,
            model=model,
            description=description,
            condition=condition,
            year=year,
            price=price,
            image=image,
            category_id=category_id  # Assign the selected category ID to the category field
        )

        return redirect('selling_details')  # Redirect to a different page after successful form submission

    return render(request, 'selling.html', context)



@never_cache 
@login_required(login_url='login')
def product_details(request):
    # Retrieve all SecondHandProduct objects
    products = SecondHandProduct.objects.all()

    # Pass the products to the template
    return render(request, 'product_details.html', {'products': products})

@never_cache
def display_products(request):
    # Filter products where action is approved
    products = SecondHandProduct.objects.all()

    # Get the Userdetails instance associated with the logged-in user, if it exists
    try:
        user_details = Userdetails.objects.get(username=request.user.username)
    except Userdetails.DoesNotExist:
        user_details = None

    if user_details:
        # Exclude products uploaded by the logged-in user
        products = products.exclude(added_by=user_details)

    query = request.GET.get('q')
    if query:
        products = products.filter(name__icontains=query)

    # Exclude products that are associated with orders
    products = products.exclude(order__isnull=False)

    return render(request, 'display_products.html', {'products': products})




@never_cache
@login_required(login_url='login')
def staff_product(request):
    # Filter products where is_available is True
    products = SecondHandProduct.objects.all()
    return render(request, 'staff_product.html', {'products': products})





@never_cache
def ecommerce(request):
    return render(request,'ecommerce.html')


@login_required(login_url='login')
@never_cache
def selling(request):
    categories = Category.objects.all()
    return render(request, 'selling.html', {'categories': categories})



@login_required(login_url='login')
@never_cache
def selling_details(request):
    # Get the currently logged-in user
    current_user = request.user

    try:
        # Retrieve the Userdetails instance associated with the current user
        user_details = Userdetails.objects.get(username=current_user.username)

        # Filter products based on the retrieved Userdetails instance
        user_products = SecondHandProduct.objects.filter(added_by=user_details)

        # Pass the filtered products to the template
        return render(request, 'selling_details.html', {'products': user_products})

    except Userdetails.DoesNotExist:
        # Handle the case where Userdetails instance does not exist for the current user
        # You can redirect the user to a page indicating that they need to set up their details
        return HttpResponse("Userdetails not found for this user.")




@never_cache
@login_required(login_url='login')
def product_approve(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        try:
            product = get_object_or_404(SecondHandProduct, pk=product_id)
            product.action = 'approved'
            product.save()
            # Redirect to the product approval page
            return redirect('product_approve')
        except SecondHandProduct.DoesNotExist:
            # Handle the case where the product does not exist
            # You can add appropriate error handling or redirect to a different page
            pass

    # Fetch all products
    products = SecondHandProduct.objects.all()
    return render(request, 'product_approve.html', {'products': products})



@never_cache
def productview(request, product_id):
    product = get_object_or_404(SecondHandProduct, pk=product_id)
    return render(request, 'productview.html', {'product': product})

@never_cache 
@login_required(login_url='login')
def exchangelist(request, product_id):
    product = get_object_or_404(SecondHandProduct, pk=product_id)
    return render(request, 'exchangelist.html', {'product': product})



@never_cache 
@login_required(login_url='login')
def delete_product(request, product_id):
    if request.method == 'POST':
        product = SecondHandProduct.objects.get(pk=product_id)
        product.is_available = False  # Set is_available to False instead of deleting
        product.save()
    return redirect('product_details') 

@never_cache 
@login_required(login_url='login')
def exchange(request, product_id):
    product = get_object_or_404(SecondHandProduct, pk=product_id)
    return render(request, 'exchange.html', {'product': product})


@never_cache
@login_required(login_url='login')
def add_to_cart(request, product_id):
    try:
        # Get the product
        product = SecondHandProduct.objects.get(pk=product_id)
        
        # Calculate the payment amount
        # Calculate the payment amount (amount * 100) and add 150 to it
        # Calculate the payment amount by adding 150 to the product price
        payment_amount = (product.price + 150) * 100


        
        # Get or create the user's cart
        cart, created = Cart.objects.get_or_create(user=request.user)

        # Get or create the cart item
        cart_item, item_created = CartItem.objects.get_or_create(product=product, cart=cart)

        if not item_created:
            # If the product is already in the cart, increase the quantity by 1
            cart_item.quantity += 1
            cart_item.save()
            return JsonResponse({'success': False, 'message': 'Product is already in the cart.'})

        return JsonResponse({'success': True, 'message': 'Product successfully added to the cart.', 'payment_amount': payment_amount})
    except SecondHandProduct.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Product not found.'})

@never_cache 
@login_required(login_url='login')
def cart_view(request):
    try:
        # Get the user's cart
        user_cart = Cart.objects.get(user=request.user)
        # Retrieve products in the cart
        products_in_cart = user_cart.products.all()
        
        # Calculate total payment amount for all items in the cart
        payment_amount = sum(item.price * 100 for item in products_in_cart)

        
        return render(request, 'cart.html', {'products_in_cart': products_in_cart, 'payment_amount': payment_amount})
    except Cart.DoesNotExist:
        # If the cart does not exist for the user
        return render(request, 'cart.html', {'products_in_cart': None})




def remove_from_cart(request, product_id):
    cart_item = get_object_or_404(CartItem, product_id=product_id, cart__user=request.user)
    cart_item.delete()
    return redirect('cart')









def add_deliveryboy(request):
    if request.method == 'POST':
        full_name = request.POST['full_name']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        
        # Create a new User object
        user = User.objects.create_user(username=username, email=email, password=password)
        
        # Create a new Deliveryboy object and save it to the database
        deliveryboy = Deliveryboy.objects.create(user=user, full_name=full_name, email=email, username=username, password=password)

        send_mail(
            'Welcome to Device Revive',
            f'Dear {full_name},\n\nYou have been added as a delivery boy. Your username is {username} and password is {password}. '
             f'Please log in with these credentials..'
              f'Remember to update your profile and change the temporary password provided.\n\n' \
              f'Thank you!\nDevice Revive',
            'your_email@example.com',  # Replace with your email address
            [email],  # Use the staff member's email address
            fail_silently=False,
        )

        return redirect('deliveryboy')  # Redirect to a success page
    else:
        return render(request, 'add_deliveryboy.html')

def deliveryboy(request):
    delivery_boys = Deliveryboy.objects.all()
    context = {
        'delivery_boys': delivery_boys
    }
    return render(request, 'deliveryboy.html', context)



@login_required(login_url='login')
@never_cache
def deliveryboyprofile(request):
    # Assuming you want to display details of the currently logged-in delivery boy
    current_user = request.user
    deliveryboy = Deliveryboy.objects.get(user=current_user)
    
    context = {
        'deliveryboy': deliveryboy
    }
    
    return render(request, 'deliveryboyprofile.html', context)



@login_required(login_url='login')
@never_cache
def deliveryboy_update(request):
    # Assuming each delivery boy has a corresponding User object
    user = request.user
    deliveryboy = Deliveryboy.objects.get(user=user)
    
    if request.method == 'POST':
        full_name = request.POST.get('fullName')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        username = request.POST.get('userName')
        street = request.POST.get('street')
        city = request.POST.get('city')
        pincode = request.POST.get('pincode')  # Retrieve pincode from form data


        # Get or create the Address object
        address, created = Address.objects.get_or_create(home_address=street, city=city, pincode=pincode)
        
        # Update delivery boy's details
        deliveryboy.full_name = full_name
        deliveryboy.email = email
        deliveryboy.phone_number = phone_number
        deliveryboy.username = username
        deliveryboy.address = address
        deliveryboy.save()
        
        return redirect('deliveryboyprofile')  # Redirect to a success page or profile page
    
    context = {
        'deliveryboy': deliveryboy
    }
    
    return render(request, 'deliveryboy_update.html', context)


@never_cache
@login_required(login_url='login')
def add_to_wishlist(request, product_id):
    try:
        # Get the product
        product = SecondHandProduct.objects.get(pk=product_id)
        
        # Get or create the user's wishlist
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)

        # Add product to wishlist
        wishlist_item, item_created = WishlistItem.objects.get_or_create(product=product, wishlist=wishlist)

        if not item_created:
            return JsonResponse({'success': False, 'message': 'Product is already in the wishlist.'})

        return JsonResponse({'success': True, 'message': 'Product successfully added to the wishlist.'})
    except SecondHandProduct.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Product not found.'})



@never_cache
@login_required(login_url='login')
def wishlist_view(request):
    try:
        # Get the user's wishlist
        user_wishlist = Wishlist.objects.get(user=request.user)
        # Retrieve products in the wishlist
        products_in_wishlist = user_wishlist.products.all()
        
        # Exclude products that are associated with orders
        products_in_wishlist = products_in_wishlist.exclude(order__isnull=False)
        
        return render(request, 'wishlist.html', {'products_in_wishlist': products_in_wishlist})
    except Wishlist.DoesNotExist:
        # If the wishlist does not exist for the user
        return render(request, 'wishlist.html', {'products_in_wishlist': None})



def remove_from_wishlist(request, product_id):
    if request.method == "POST":
        product = SecondHandProduct.objects.get(pk=product_id)
        user_wishlist = Wishlist.objects.get(user=request.user)
        wishlist_item = WishlistItem.objects.get(product=product, wishlist=user_wishlist)
        wishlist_item.delete()
        return redirect('wishlist')  # Redirect back to the wishlist page after removal
    return redirect('wishlist')  # Redirect back to the wishlist page if not a POST request


@login_required(login_url='login')
def add_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            Category.objects.create(name=name)
            return redirect('categorylist')  # Replace 'success_page' with the URL name of the page you want to redirect to after successful form submission
    return render(request, 'add_category.html')


@login_required(login_url='login')
def category_list_view(request):
    categories = Category.objects.all()
    return render(request, 'categorylist.html', {'categories': categories})


@never_cache
@login_required(login_url='login')
def pickup(request):
    products = SecondHandProduct.objects.filter(is_picked_up=False)
    context = {
        'products': products,
    }
    return render(request, 'pickup.html', context)


@never_cache
@login_required(login_url='login')
def fulldetails(request, product_id):
    product = SecondHandProduct.objects.get(id=product_id)
    
    if request.method == 'POST':
        is_picked_up = request.POST.get('picked_up')
        
        if is_picked_up == 'on':
            product.is_picked_up = True
        else:
            product.is_picked_up = False
        
        product.save()
        return redirect('fulldetails', product_id=product_id)
    
    context = {
        'product': product,
    }
    
    return render(request, 'fulldetails.html', context)



@never_cache
@login_required(login_url='login')
def edit_product(request, product_id):
    product = get_object_or_404(SecondHandProduct, id=product_id)
    categories = Category.objects.all()  # Assuming you have imported the Category model
    return render(request, 'edit_product.html', {'product': product, 'categories': categories})


@never_cache
@login_required(login_url='login')
def update_second_hand_product(request, product_id):
    product = get_object_or_404(SecondHandProduct, id=product_id)
    
    if request.method == 'POST':
        # Retrieve the category object based on the submitted category ID
        category_id = request.POST.get('category')
        category = get_object_or_404(Category, id=category_id)
        
        # Update the product details
        product.category = category
        product.brand = request.POST.get('brand')
        product.model = request.POST.get('model')
        product.description = request.POST.get('description')
        product.condition = request.POST.get('condition')
        product.year = request.POST.get('year')
        product.price = request.POST.get('price')
        
        if 'image' in request.FILES:
            product.image = request.FILES['image']
        
        product.save()
        
        return redirect('selling_details') 
    
@never_cache
@login_required(login_url='login')
def save_new_address(request):
    if request.method == 'POST':
        home_address = request.POST.get('homeAddress')
        city = request.POST.get('city')
        pincode = request.POST.get('pincode')
        product_id = request.POST.get('product_id')  # Assuming you have product_id in your form
        
        # Retrieve the logged-in user
        user_details = Userdetails.objects.get(username=request.user.username)
        
        # Create a new Address object and save it
        new_address = Address.objects.create(home_address=home_address, city=city, pincode=pincode)
        
        # Update the address field of the Userdetails model for the logged-in user
        user_details.address = new_address
        user_details.save()
        
        # Assuming you want to redirect to 'buynow' with the retrieved product_id
        return redirect('buynow', product_id=product_id)  # Redirect to buynow with product_id
    else:
        return redirect('error_url')

@never_cache
@login_required(login_url='login')
def delivery_details(request):
    # Exclude orders with delivery status 'Delivered'
    orders = Order.objects.exclude(delivery_status='Delivered').select_related('cart', 'user', 'product')
    return render(request, 'delivery_details.html', {'orders': orders})


@never_cache
@login_required(login_url='login')
def view_order_details(request, order_id):
    try:
        order = Order.objects.get(pk=order_id)
        return render(request, 'view_order_details.html', {'order': order})
    except Order.DoesNotExist:
        return render(request, 'view_order_details.html', {'error_message': 'Order does not exist.'})

@never_cache
@login_required(login_url='login')
def buynow(request, product_id):
    try:
        # Get the product details
        product = get_object_or_404(SecondHandProduct, pk=product_id)
        
        # Get or create the user's cart
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_id = cart.id
        
        # Calculate the payment amount (amount * 100)
        payment_amount = product.price * 100
        total_amount = payment_amount/100
        
        # Get the user details of the logged-in user
        user_details = Userdetails.objects.get(username=request.user.username)
        
        # Create the order with user, product, and cart information
        order = Order.objects.create(cart=cart, user=user_details, product=product, total_amount=total_amount)

        # Pass the product, payment amount, and cart ID to the template
        return render(request, 'buynow.html', {'product': product, 'payment_amount': payment_amount, 'total_amount': total_amount,'cart_id': cart_id, 'user_details': user_details})
    except SecondHandProduct.DoesNotExist:
        return JsonResponse({'error': 'Product not found.'}, status=404)





@never_cache
@login_required(login_url='login')
def my_order(request):
    # Get the currently logged-in user
    current_user = request.user

    try:
        # Retrieve the Userdetails instance associated with the current user
        user_details = Userdetails.objects.get(username=current_user.username)

        # Filter orders based on the retrieved Userdetails instance
        user_orders = Order.objects.filter(user=user_details)

        # Pass the filtered orders to the template
        return render(request, 'my_order.html', {'user_orders': user_orders})

    except Userdetails.DoesNotExist:
        # Handle the case where Userdetails instance does not exist for the current user
        # You can redirect the user to a page indicating that they need to set up their details
        return HttpResponse("Userdetails not found for this user.")


@never_cache
@login_required(login_url='login')
def update_delivery_status(request, order_id):
    order = get_object_or_404(Order, pk=order_id)

    if request.method == 'POST':
        status = request.POST.get('delivery_status')

        if status == 'delivered':
            # Generate OTP
            otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])

            # Send OTP to the buyer's email
            send_mail(
                'OTP for Delivery Status Verification',
                f'Your OTP for verifying delivery status is: {otp}',
                settings.EMAIL_HOST_USER,  # Sender's email
                [order.user.email],  # Buyer's email
                fail_silently=False,
            )

            # Store OTP in session
            request.session['delivery_status_otp'] = otp

            # Redirect to OTP verification page
            return redirect('otp_verification', order_id=order_id)
        else:
            order.delivery_status = status
            order.save()
            return redirect('delivery_details')
    else:
        pass


@never_cache
@login_required(login_url='login')
def otp_verification(request, order_id):
    order = get_object_or_404(Order, pk=order_id)

    # Retrieve the OTP from session
    otp_from_session = request.session.get('delivery_status_otp')

    if request.method == 'POST':
        # Get the submitted OTP
        submitted_otp = request.POST.get('otp')

        # Verify the submitted OTP
        if submitted_otp == otp_from_session:
            # OTP is verified, update the delivery status
            order.delivery_status = 'Delivered'  # Marking the order as delivered
            order.save()

            # Clear OTP from session
            del request.session['delivery_status_otp']

            # Redirect to delivery details page
            return redirect('delivery_success')
        else:
            # OTP is incorrect, render the OTP verification page with error message
            return render(request, 'otp_verification.html', {'error_message': 'Incorrect OTP'})

    else:
        # Render the OTP verification page
        return render(request, 'otp_verification.html', {'order': order})


@never_cache
@login_required(login_url='login')
def delivery_success(request):
    
    return render(request, 'delivery_success.html')


@never_cache
@login_required(login_url='login')
def apply_leave(request):
    # Initialize total_leaves_taken
    total_leaves_taken = 0
    remaining_leaves = 0

    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        number_of_days = request.POST.get('number_of_days')
        reason = request.POST.get('reason')
        if start_date and end_date and number_of_days and reason:
            # Get the current year
            current_year = datetime.now().year
            # Calculate total leaves taken by the delivery boy in the current year
            total_leaves_taken = LeaveApplication.objects.filter(
                staff=request.user.deliveryboy,
                start_date__year=current_year
            ).aggregate(total_leaves=Sum('number_of_days'))['total_leaves'] or 0
            # Calculate maximum leaves allowed
            max_leaves_allowed = 20
            # Calculate remaining leaves
            remaining_leaves = max_leaves_allowed - total_leaves_taken
            # Check if the total leaves taken plus the requested leaves exceed the maximum allowed
            if total_leaves_taken + int(number_of_days) <= max_leaves_allowed:
                if request.user.deliveryboy:  
                    LeaveApplication.objects.create(
                        staff=request.user.deliveryboy,
                        start_date=start_date,
                        end_date=end_date,
                        number_of_days=number_of_days,
                        reason=reason
                    )
                    messages.success(request, 'Leave application submitted successfully!')
                    return redirect('leave_status')
                else:
                    messages.error(request, 'You are not a delivery boy.')
            else:
                messages.error(request, 'Exceeds maximum leaves allowed for the year.')
        else:
            messages.error(request, 'Please fill in all the fields')

    # Calculate remaining leaves
    total_leaves_taken = LeaveApplication.objects.filter(
        staff=request.user.deliveryboy,
        start_date__year=datetime.now().year
    ).aggregate(total_leaves=Sum('number_of_days'))['total_leaves'] or 0

    max_leaves_allowed = 20
    remaining_leaves = max_leaves_allowed - total_leaves_taken
    remaining_leaves = max(0, remaining_leaves)

    return render(request, 'apply_leave.html', {'max_leaves_allowed': max_leaves_allowed, 'remaining_leaves': remaining_leaves})

@never_cache
@login_required(login_url='login')
def leave_status(request):
    try:
        deliveryboy = request.user.deliveryboy
        staff_leave_applications = LeaveApplication.objects.filter(staff=deliveryboy)
        return render(request, 'leave_status.html', {'leave_applications': staff_leave_applications})
    except ObjectDoesNotExist:
        error_message = "User has no associated Deliveryboy object."
        return render(request, 'apply_leave.html', {'error_message': error_message})

@never_cache
@login_required(login_url='login')
def leave_applications(request):
    leave_requests = LeaveApplication.objects.select_related('staff').all()
    return render(request, 'leave_applications.html', {'leave_requests': leave_requests})

@never_cache
@login_required(login_url='login')
def approve_leave(request, leave_application_id):
    leave_application = get_object_or_404(LeaveApplication, pk=leave_application_id)

    if request.method == 'POST':
        leave_application.status = 'Approved'
        leave_application.save()

        # Subtract approved leave days from total leaves taken
        total_leaves_taken = LeaveApplication.objects.filter(
            staff=leave_application.staff,
            start_date__year=datetime.now().year,
            status='Approved'
        ).aggregate(total_leaves=Sum('number_of_days'))['total_leaves'] or 0

        # Update remaining leaves for the delivery boy
        max_leaves_allowed = 20
        remaining_leaves = max_leaves_allowed - total_leaves_taken

        subject = 'Leave Application Approved'
        message = 'Your leave application has been approved.'
        from_email = 'device_revive@email.com'  
        to_email = leave_application.staff.email
        send_mail(subject, message, from_email, [to_email])

        return redirect('leave_applications')

    return render(request, 'leave_applications.html', {'leave_application': leave_application})




    #chatgpt nrs
    # chatapp/views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from transformers import GPT2LMHeadModel, GPT2Tokenizer

model_name = "gpt2"
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(model_name)



@never_cache
@login_required(login_url='login')
@csrf_exempt
def chatgpt(request):
    return render(request, 'chatgpt.html')

@csrf_exempt
def generate_response(request):
    if request.method == 'POST':
        user_input = request.POST.get('user_input')
        response = generate_gpt2_response(user_input)
        return JsonResponse({'response': response})
    else:
        return JsonResponse({'error': 'Invalid request method'})

def generate_response(request):
    if request.method == 'POST':

        user_input = request.POST.get('user_input').lower()
        if 'slow' in user_input:
            response_data = {'response': "Slow performance can be due to various reasons. You can try the following:\n\n- Close unused programs and browser tabs.\n- Delete temporary files and clear cache.\n- Disable startup programs.\n- Increase RAM or upgrade to an SSD."}
        elif 'internet connectivity' in user_input:
            response_data = {'response': "If you're experiencing internet connectivity issues:\n\n- Restart your router and modem.\n- Check if other devices can connect to the same network.\n- Update network drivers.\n- Reset TCP/IP stack or renew IP address."}
        elif 'overheating' in user_input:
            response_data = {'response': "If your laptop/computer is overheating:\n\n- Ensure proper ventilation and avoid blocking air vents.\n- Clean dust from fans and heat sinks.\n- Use a laptop cooling pad.\n- Avoid using the device on soft surfaces like beds or sofas."}
        elif 'frozen' in user_input:
            response_data = {'response': "If your laptop/computer is frozen:\n\n- Press Ctrl + Alt + Delete to open Task Manager.\n- End unresponsive tasks or processes.\n- Restart your device if necessary.\n- Check for updates and install them."}
        elif 'turn on' in user_input:
            response_data = {'response': "If your laptop/computer won't turn on:\n\n- Check power connections and try a different outlet.\n- Remove the battery (if removable) and reinsert it.\n- Press and hold the power button for 10-15 seconds.\n- Test with a different power adapter or charger."}
        elif 'error messages' in user_input:
            response_data = {'response': "If your laptop/computer is showing strange error messages:\n\n- Note down the error message and search online for solutions.\n- Update device drivers and system software.\n- Run a malware scan using antivirus software.\n- If the issue persists, consider seeking professional help."}
        # Add more questions and answers related to computer/laptop issues here
        elif 'battery life' in user_input:
            response_data = {'response': "To improve battery life:\n\n- Lower screen brightness.\n- Disable background processes and apps.\n- Use battery saver mode.\n- Avoid extreme temperatures."}
        elif 'storage space' in user_input:
            response_data = {'response': "If you're running out of storage space:\n\n- Delete unnecessary files and programs.\n- Move files to external storage or cloud storage.\n- Use disk cleanup tools.\n- Consider upgrading to a larger hard drive or SSD."}
        elif 'blue screen' in user_input:
            response_data = {'response': "If you're encountering blue screen errors:\n\n- Update device drivers.\n- Scan for malware.\n- Check for hardware issues such as faulty RAM or hard drive.\n- Restore system to a previous state using System Restore (Windows) or Time Machine (Mac)."}
        elif 'hi' in user_input:
            response_data={'response':"hello"}
        else:
            response_data = {'response': "Sorry, I couldn't understand. Please rephrase your question."}
            # response = generate_gpt2_response(user_input)
            # response_data = {'response': response}

        return JsonResponse(response_data)
    else:
        return JsonResponse({'error': 'Invalid request method'})


def generate_gpt2_response(user_input, max_length=100):
    input_ids = tokenizer.encode(user_input, return_tensors="pt")
    output = model.generate(input_ids, max_length=max_length, num_beams=5, no_repeat_ngram_size=2, top_k=50, top_p=0.95)
    response = tokenizer.decode(output[0], skip_special_tokens=True)
    return response



# from django.shortcuts import render
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# import pandas as pd
# from sklearn.model_selection import train_test_split
# from sklearn.preprocessing import LabelEncoder
# from sklearn.ensemble import RandomForestRegressor
# from sklearn.metrics import mean_squared_error

# # Load the dataset
# data = pd.read_csv("templates/laptops.csv", encoding='latin1')
# data.dropna(inplace=True)

# # Preprocess: Replace commas with periods in the 'Price (Euros)' column
# data['Price (Euros)'] = data['Price (Euros)'].str.replace(',', '.').astype(float)

# # Encode categorical variables
# label_encoder_manufacturer = LabelEncoder()
# label_encoder_model = LabelEncoder()
# data['Manufacturer'] = label_encoder_manufacturer.fit_transform(data['Manufacturer'])
# data['Model Name'] = label_encoder_model.fit_transform(data['Model Name'])

# # Feature selection
# X = data[['Manufacturer', 'Model Name']]
# y = data['Price (Euros)']

# # Split the dataset into training and testing sets
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# # Train the Random Forest model
# rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
# rf_model.fit(X_train, y_train)



# @never_cache
# @login_required(login_url='login')
# @csrf_exempt
# def predict_price(request):
#     if request.method == 'POST':
#         try:
#             manufacturer = request.POST.get('manufacturer')
#             model_name = request.POST.get('model_name')
#             # Encode manufacturer and model name
#             manufacturer_encoded = label_encoder_manufacturer.transform([manufacturer])[0]
#             model_name_encoded = label_encoder_model.transform([model_name])[0]
#             # Predict the price using the trained Random Forest model
#             predicted_price = rf_model.predict([[manufacturer_encoded, model_name_encoded]])[0]
#             # Find details of the laptop
#             details = data[(data['Manufacturer'] == manufacturer_encoded) & (data['Model Name'] == model_name_encoded)].iloc[0]
#             # Prepare the response
#             response_data = {
#                 'predicted_price': predicted_price,
#                 'details': {
#                     'Manufacturer': manufacturer,
#                     'Model Name': model_name,
#                     'Details': details.to_dict()
#                 }
#             }
#             # Pass the response data to the prediction_result.html template
#             return render(request, 'prediction_result.html', response_data)
#         except ValueError as e:
#             error_message = "An error occurred while processing the request: " + str(e)
#             return render(request, 'seminar.html', {'error_message': error_message})  # Render seminar.html with error message
#         except IndexError as e:
#             error_message = "An error occurred while processing the request: " + str(e)
#             return render(request, 'seminar.html', {'error_message': error_message})  # Render seminar.html with error message
#     else:
#         return render(request, 'seminar.html')



@never_cache
@login_required(login_url='login')
def seminar(request):
    error_message = '{"error": "An error occurred while processing the request: single positional indexer is out-of-bounds"}'
    return render(request, 'seminar.html', {'error_message': error_message})



@never_cache
@login_required(login_url='login')
def prediction_result(request):
    # You can pass any necessary context data here if needed
    return render(request, 'prediction_result.html')




import base64
from django.shortcuts import render
from django.http import JsonResponse
import google.generativeai as genai

# Configure GenAI
genai.configure(api_key="AIzaSyA7DEI4vUWqZiOiv7V3WbWLIokWlA7jT0I")

# Set up the model and safety settings
generation_config = {
    "temperature": 0.4,
    "top_p": 1,
    "top_k": 32,
    "max_output_tokens": 4096,
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
]

model = genai.GenerativeModel(model_name="gemini-1.0-pro-vision-latest",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

from django.shortcuts import render
from django.http import JsonResponse
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
import numpy as np

# Load the dataset
data = pd.read_csv("static/laptops.csv", encoding='latin1')

# Remove rows with NaN values in the target variable and rename the column
data.dropna(subset=['Price (Euros)'], inplace=True)
data['Price (Euros)'] = data['Price (Euros)'].str.replace(',', '.').astype(float)
data.rename(columns={'Price (Euros)': 'Price'}, inplace=True)

# Encode categorical variables
label_encoder_model = LabelEncoder()
data['Model Name'] = label_encoder_model.fit_transform(data['Model Name'])

# Fill NaN values in the DataFrame with an empty string
data.fillna('', inplace=True)

# Features and target variable
X = data[['Model Name']]
y = data['Price']

# Train the model
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X, y)

def predict_details(request):
    if request.method == 'POST' and 'model_name' in request.POST:
        model_name = request.POST['model_name']
        try:
            # Transform model name using the same label encoder
            model_name_encoded = label_encoder_model.transform([model_name])[0]
            # Predict laptop details
            predicted_price = rf_model.predict([[model_name_encoded]])[0]
            details = data[data['Model Name'] == model_name_encoded].iloc[0].to_dict()
            details['Predicted Price'] = predicted_price
            return JsonResponse({'success': True, 'details': details})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    else:
        return JsonResponse({'success': False, 'error': 'Model name not provided'})



def upload_image(request):
    if request.method == 'POST' and request.FILES['image']:
        image_file = request.FILES['image']
        image_bytes = image_file.read()

        # Generate prompt parts
        image_part = {
            "mime_type": "image/jpeg",
            "data": image_bytes
        }
        prompt_parts = [image_part, "what is model name this laptop?\n"]

        # Generate response from model
        response = model.generate_content(prompt_parts)
        model_name = response.text.strip()

        # Encode the image bytes to base64
        encoded_image = base64.b64encode(image_bytes).decode('utf-8')

        # Pass the model name and encoded image in the JSON response
        return JsonResponse({'model_name': model_name, 'encoded_image': encoded_image})
    else:
        return JsonResponse({'error': 'Image file not found or invalid'})
