from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth import authenticate,login
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib import auth
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from.models import Userdetails
#create your views here
def index(request):
    return render(request,'index.html')
def loginn(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user) 
            messages.success(request, 'Login successful!')
            return redirect('userprofile')
        else:
            messages.error(request,'Invalid username or password')  # Add an error message
            return redirect('login')  # Redirect back to the login page

    return render(request, 'login.html')

    
    
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



def services(request):
    return render(request,'services.html')
def userprofile(request):
    return render(request,'userprofile.html')
def about(request):
    return render(request,'about.html')
def contact(request):
    return render(request,'contact.html')
def booking(request):
    return render(request,'booking.html')
def desktop(request):
    return render(request,'desktop.html')
def laptop(request):
    return render(request,'laptop.html')
def why(request):
    return render(request,'why.html')
def after_login(request):
    return render(request,'after_login.html')
def logout (request):
    auth.logout(request)
    return redirect('/')
