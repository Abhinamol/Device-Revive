from django.urls import path
from.import views

urlpatterns = [
    path('',views.index,name="index"),
    path('index',views.index,name="index"),
    path('login',views.loginn,name="login"),
    path('signup',views.signup,name="signup"),
    path('services',views.services,name="services"),
    path('about',views.about,name="about"),
    path('contact',views.contact,name="contact"),
    path('booking',views.booking,name="booking"),
    path('why',views.why,name="why"),
    path('desktop',views.desktop,name="desktop"),
    path('laptop',views.laptop,name="laptop"),
    path('userprofile',views.userprofile,name="userprofile"),
    path('after_login',views.after_login,name="after_login"),
    path('logout',views.logout,name="logout"),
    path('check_username_availability/', views.check_username_availability, name='check_username_availability'),
    path('check_email_availability/', views.check_email_availability, name='check_email_availability'),
    
     
]
