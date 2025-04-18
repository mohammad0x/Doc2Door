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
    path('singlePost/<slug:slug>' ,singlePost , name='singlePost' ),
    path('category/<slug:slug>', category ,name="category"),
]
