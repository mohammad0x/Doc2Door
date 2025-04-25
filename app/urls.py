from django.urls import path
from .views import *

app_name = 'app'


urlpatterns = [
    path('home/' ,Home , name='home' ),

    path('logout/' ,Logout_view , name='logout' ),
    path('loginPhone/' , login_phone , name='loginPhone'),
    path('verify_login_phone/' , verify_login_phone , name='verify_login_phone'),
    path('loginPhoneDoctor/' , login_phone_doctor , name='loginPhoneDoctor'),
    path('verify_login_phone_doctor/' , verify_login_phone_doctor , name='verify_login_phone_doctor'),

    path('updateProfile/' , ProfileUpdate ,name='ProfileUpdate'),
    path('profile/' , profile_view ,name='profile'),

    path('post/',postView , name="postView"),
    path('singlePost/<str:slug>' ,singlePost , name='singlePost' ),
    path('category/<str:slug>', category ,name="category"),

    path('news/',newsView , name="newsView"),
    path('singleNews/<str:slug>',singleNews , name="singleNews"),

    path('reservationView/<int:id>' , reservationView , name='reservationView'),
    path('showReservation/' , showReservation , name="showReservation"),
    path('reservationRequest/<int:id>' , reservationRequest , name='reservationRequest'), 
    path('cartView/' , cartView , name='cartView'),

    path('send_request/', request_payment, name='request'),
    path('verify/', verify , name='verify'),
]
