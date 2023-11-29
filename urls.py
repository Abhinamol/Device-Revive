from django.urls import path
from.import views
from django.contrib.auth import views as auth_views
from .views import staff_update
from .views import staff_profile
from .views import delete_staff
from .views import check_service_name

urlpatterns = [
    path('',views.index,name="index"),
    path('index',views.index,name="index"),
    path('login',views.loginn,name="login"),
    path('signup',views.signup,name="signup"),
    path('services',views.services,name="services"),
    path('about',views.about,name="about"),
    path('contact',views.contact,name="contact"),
    path('bookingconfirmation',views.bookingconfirmation,name="bookingconfirmation"),
    path('booking/', views.booking, name="booking"),

    path('why',views.why,name="why"),
    
    path('desktop',views.desktop,name="desktop"),
    path('booknow',views.booknow,name="booknow"),
    path('userprofile',views.userprofile,name="userprofile"),
    path('myprofile',views.myprofile,name="myprofile"),
    path('staff_profile/', staff_profile, name='staff_profile'),
    path('update',views.update,name="update"),
    path('after_login',views.after_login,name="after_login"),
    path('logout',views.logout,name="logout"),

     

    path('check_username_availability/', views.check_username_availability, name='check_username_availability'),
    path('check_email_availability/', views.check_email_availability, name='check_email_availability'),
   
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    
    path('userdetailss', views.userdetailss, name='userdetailss'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('servicedetails', views.servicedetails, name='servicedetails'),
    path('edit_service/', views.edit_service, name='edit_service'),
    path('staffs', views.staffs, name='staffs'),
    path('updateuser', views.updateuser, name='updateuser'),

    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('add_service', views.add_service, name='add_service'),
    path('delete_service/<int:service_id>/', views.delete_service, name='delete_service'),
    path('update_service/<int:service_id>/', views.update_service, name='update_service'),
    path('edit_service/<int:service_id>/', views.edit_service, name='edit_service'),
    path('book-now/<int:service_id>/', views.book_now, name='book_now'),
    path('add_staff/', views.add_staff, name='add_staff'),
   
    path('delete_staff/<int:staff_id>/', delete_staff, name='delete_staff'),
    path('staff/update/', staff_update, name='staff_update'),
    path('check_service_name/', check_service_name, name='check_service_name'),
    
    
    
    
    

]

    

    
    
     

