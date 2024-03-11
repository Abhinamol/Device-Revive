from django.urls import path
from.import views
from django.contrib.auth import views as auth_views
from .views import staff_update
from .views import staff_profile
from .views import delete_staff
from .views import check_service_name
from .views import booking_details
from .views import verify_payment
from .views import confirm_booking
from .views import admin_booking
from django.conf import settings
from django.conf.urls.static import static
from .views import productview
from .views import add_deliveryboy
from .views import add_to_wishlist, wishlist_view

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
    path('booking_details/', booking_details, name='booking_details'),
    path('verify_payment/', verify_payment, name='verify_payment'),
    path('confirm_booking/', confirm_booking, name='confirm_booking'),
    path('admin_booking/', admin_booking, name='admin_booking'),

    path('why',views.why,name="why"),
    path('ecommerce',views.ecommerce,name="ecommerce"),
    
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
    path('staff_services', views.staff_services, name='staff_services'),
    path('updateuser', views.updateuser, name='updateuser'),
    path('product_details', views.product_details, name='product_details'),
    
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('add_service', views.add_service, name='add_service'),
    path('delete_service/<int:service_id>/', views.delete_service, name='delete_service'),
    path('update_service/<int:service_id>/', views.update_service, name='update_service'),
    path('edit_service/<int:service_id>/', views.edit_service, name='edit_service'),
    path('book-now/<int:service_id>/', views.book_now, name='book_now'),
    path('add_staff/', views.add_staff, name='add_staff'),
    path('add_product/', views.add_second_hand_product, name='add_second_hand_product'),
    path('display_products/', views.display_products, name='display_products'),
    path('staff_product/', views.staff_product, name='staff_product'),

    path('delete_staff/<int:staff_id>/', delete_staff, name='delete_staff'),
    path('staff/update/', staff_update, name='staff_update'),
    path('check_service_name/', check_service_name, name='check_service_name'),
    path('review/',views.Review_rate,name="review"),
   
    path('delete_product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('exchange/<int:product_id>/', views.exchange, name='exchange'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart'),
    path('productview/<int:product_id>/', views.productview, name='productview'),
    path('remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('exchangelist/<int:product_id>/', views.exchangelist, name='exchangelist'),
    path('selling/', views.selling, name='selling'),
    path('selling_details/', views.selling_details, name='selling_details'),
    path('product_approve/', views.product_approve, name='product_approve'),
    path('buynow/<int:product_id>/', views.buynow, name='buynow'),
    path('add_deliveryboy/', views.add_deliveryboy, name='add_deliveryboy'),
    path('deliveryboy/', views.deliveryboy, name='deliveryboy'),
    path('deliveryboyprofile/', views.deliveryboyprofile, name='deliveryboyprofile'),
    path('deliveryboy_update/', views.deliveryboy_update, name='deliveryboy_update'),
    path('add-to-wishlist/<int:product_id>/', add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/', wishlist_view, name='wishlist'),
    path('remove_from_wishlist/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('add_category/', views.add_category, name='add_category'),
    path('categorylist/', views.category_list_view, name='categorylist'),
    path('pickup/', views.pickup, name='pickup'),
    path('fulldetails/<int:product_id>/', views.fulldetails, name='fulldetails'),
    
   


    

    
]

    
    

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  
    
     

