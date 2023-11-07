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
from .models import Service
from .models import Technician
from django.contrib.auth.hashers import check_password 






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

            messages.success(request, 'Login successful!')
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
@login_required(login_url='login')
def staff_profile(request):
    return render(request,'staff_profile.html')


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
def booknow(request):
    return render(request,'booknow.html')


@never_cache
@login_required(login_url='login')
def bookingconfirmation(request):
    return render(request,'bookingconfirmation.html')


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
        # Update user details and address based on form data
        user_details = Userdetails.objects.get(username=request.user.username)
        user_details.full_name = request.POST.get('full-name')
        user_details.email = request.POST.get('eMail')
        user_details.phone = request.POST.get('phone')
        user_details.username = request.POST.get('username')
        user_details.save()

        if user_details.address:
            address = user_details.address
        else:
            address = Address()

        address.home_address = request.POST.get('home')
        address.city = request.POST.get('city')
        address.pincode = request.POST.get('zip')
        address.save()
        
        # Redirect to the profile page
        return redirect('profile')

    # Assuming you have a Userdetails object associated with the user
    user_details = Userdetails.objects.get(username=request.user.username)

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
           
        )
        technician.save()

        # Redirect to a different page after adding the technician
        return redirect('staffs')  # Redirect to the technician list view

    return render(request, 'add_staff.html')


@never_cache
@login_required
def staffs(request):
    staff_data = Technician.objects.all()  # Fetch all staff data from the database

    context = {
        'staff_data': staff_data,
    }

    return render(request, 'staffs.html', context)


def delete_staff(request, staff_id):
    if request.method == 'POST':
        try:
            # Retrieve the technician from the database
            technician = get_object_or_404(Technician, pk=staff_id)

            # Delete the technician
            technician.delete()

            # Return a success response
            return redirect('staffs')
        except Technician.DoesNotExist:
            return JsonResponse({'error': 'Technician not found'}, status=404)

    return JsonResponse({'error': 'Invalid request method'}, status=405)
