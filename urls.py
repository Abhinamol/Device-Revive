from django.urls import path
from.import views
from django.contrib.auth import views as auth_views

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
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    
     
]
