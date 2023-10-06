from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth import authenticate,login
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib import auth
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from.models import Userdetails
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

#create your views here
@never_cache
def index(request):
    return render(request,'index.html')

def loginn(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            request.session['username'] = user.username
            if username == 'admin' and password == 'admin':
                
                return redirect('adminpage')  # Redirect admin to the admin page
            else:
                messages.success(request, 'Login successful!')
                return redirect('userprofile') 
               
           
        else:
            messages.error(request,'Invalid username or password')  # Add an error message
            return redirect('login')  # Redirect back to the login page

    response = render(request,"login.html")
    response['Cache-Control'] = 'no-store,must-revalidate'
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

    

def adminpage(request):
    return render(request, 'adminpage.html') 

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
def booking(request):
    return render(request,'booking.html')

@never_cache
@login_required(login_url='login')
def desktop(request):
    return render(request,'desktop.html')

@never_cache
@login_required(login_url='login')
def laptop(request):
    return render(request,'laptop.html')

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


@login_required
def userprofile(request):
    # Get the user's name
    username = request.user.username

    # Pass the user's name to the template
    return render(request, 'userprofile.html', {'username': username})


