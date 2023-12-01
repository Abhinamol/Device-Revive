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
from .models import Booking
import datetime





#create your views here
@never_cache
def index(request):
    return render(request,'index.html')




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
                    return redirect("staff_profile")  # Redirect to staff_profile for Technicians
            except Technician.DoesNotExist:
                pass  # No Technician with this username

            
            return redirect('myprofile')
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
@login_required(login_url='/login/')
def staff_profile(request):
    # Get the current user
    user = request.user

    if request.method == 'POST':
        # Update the Technician model details
        technician = Technician.objects.get(username=user.username)
        technician.full_name = request.POST.get('fullName')
        technician.email = request.POST.get('eMail')
        technician.phone_number = request.POST.get('phone')
        technician.website = request.POST.get('website')
        technician.street = request.POST.get('Street')
        technician.city = request.POST.get('ciTy')
        technician.state = request.POST.get('sTate')
        technician.zip_code = request.POST.get('zIp')
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


 
   
@login_required(login_url='login')
def bookingconfirmation(request):
    
    
    booking = Booking.objects.latest('id')

    # Pass the relevant details to the template
    context = {
        'selected_services': booking.selected_services.all(),
        'total_cost': booking.total_service_cost,
        'selected_date': booking.preferred_date,
        'selected_time': booking.preferred_time,
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
@login_required
def servicedetails(request):
    services = Service.objects.all()
    return render(request, 'servicedetails.html', {'services': services})




@never_cache
@login_required
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
    # Your booking logic here

    # After handling the booking logic, redirect to the "booknow.html" page or any other relevant page
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
    staff = get_object_or_404(Technician, id=staff_id)
    staff.delete()
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
@login_required()
def staff_update(request):
    technicians = Technician.objects.all()

    # Try to get the associated Technician object or create a new one
    technician, created = Technician.objects.get_or_create(user=request.user)

    if request.method == "POST":
        technician.full_name = request.POST["full_name"]
        technician.email = request.POST["email"]
        technician.phone_number = request.POST["phone"]
        technician.username = request.POST["username"]
        technician.save()

        if not technician.address:
            address = Address()
        else:
            address = technician.address

        address.home_address = request.POST["home"]
        address.city = request.POST["city"]
        address.pincode = request.POST["zip"]
        address.save()

        # Update technician.address with the newly created or existing Address object
        technician.address = address

    return render(request, "staff_update.html", {'technicians': technicians, 'addressid': technician.address.id if technician.address else None})



@never_cache
@login_required
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


        # Calculate total service cost
        services = Service.objects.all()
        

        # Create a new Booking instance after calculating the total_cost
        booking_instance = Booking(
            device_type=device_type,
            brand=brand,
            model=model,
            preferred_date=preferred_date,
            preferred_time=preferred_time,
            total_service_cost=total_cost,
        )
        booking_instance.save()

        # Add selected services to the ManyToManyField
        booking_instance.selected_services.set(selected_services)

        return redirect('bookingconfirmation')  # Redirect to a success page

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
    user_details = Userdetails.objects.get(username=request.user.username)


    context = {
        'user_details': user_details,
        'laptop_brand_choices': laptop_brand_choices,
        'services': services,
        'total_cost': total_cost,
          # Include total_cost in the context
    }

    return render(request, 'booknow.html', context)


@csrf_exempt
def check_service_name(request):
    if request.method == 'GET':
        service_name = request.GET.get('name', '')
        service_exists = Service.objects.filter(name__iexact=service_name).exists()
        return JsonResponse({'exists': service_exists})