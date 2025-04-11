from django.shortcuts import render
from .models import MyUser
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import *
import random
from kavenegar import *


# Create your views here.
@login_required(login_url='/loginPhone/')
def Home(request):
    return render(request, 'app/home.html')


@login_required(login_url='/loginPhone/')
def Logout_view(request):
    logout(request)
    return redirect('app:loginPhone')


def login_phone(request):
    if request.user.is_authenticated:
        return redirect('app:home')
    if request.method == 'POST':
        global phone, random_code
        phone = request.POST.get('phone')
        random_code = random.randint(1000, 9999)
        sms = KavenegarAPI(
            "65506D4C414E3873434C4A54377862786272764342653867506E46792B2B4F624849494C5269645A66486F3D")  #
        params = {
            'sender': '2000660110',
            'receptor': phone,  # 
            'message': f' {random_code} سلام این اولین تست است ',
        }
        response = sms.sms_send(params)
        return redirect('app:verify_login_phone')

    return render(request, 'app/phone/login-phone.html')


def verify_login_phone(request):
    if request.user.is_authenticated:
        return redirect('app:home')
    if request.method == 'POST':
        form = CodePhoneForm(request.POST)
        if form.is_valid():
            if str(random_code) == form.cleaned_data['verify_code']:

                if MyUser.objects.filter(phone=phone).exists():
                    user = authenticate(request, phone=phone)
                    if user is not None:
                        login(request, user)
                        return redirect('app:home')

                # sign up
                user = MyUser.objects.create_user(phone=phone)
                user.save()

                # sign in
                user = authenticate(request, phone=phone)
                print(user)
                if user is not None:
                    login(request, user)

                global verify
                verify = True
                return redirect('app:login')
            else:
                messages.error(request, 'کد وارد شده اشتباه است')
    else:
        form = CodePhoneForm()
    context = {
        'form': form,
    }
    return render(request, 'app/phone/verify-login-phone.html', context)


def login_phone_doctor(request):
    if request.user.is_authenticated:
        return redirect('app:home')
    if request.method == 'POST':
        global phone, random_code
        phone = request.POST.get('phone')
        random_code = random.randint(1000, 9999)
        sms = KavenegarAPI(
            "65506D4C414E3873434C4A54377862786272764342653867506E46792B2B4F624849494C5269645A66486F3D")  #
        params = {
            'sender': '2000660110',
            'receptor': phone,  # 
            'message': f' {random_code} سلام این اولین تست است ',
        }
        response = sms.sms_send(params)
        return redirect('app:verify_login_phone_doctor')

    return render(request, 'app/phone/login-phone-doctor.html')


def verify_login_phone_doctor(request):
    if request.user.is_authenticated:
        return redirect('app:home')
    if request.method == 'POST':
        form = CodePhoneDoctorForm(request.POST)
        if form.is_valid():
            if str(random_code) == form.cleaned_data['verify_code']:

                if MyUser.objects.filter(phone=phone).exists():
                    user = authenticate(request, phone=phone)
                    if user is not None:
                        login(request, user)
                        return redirect('app:home')

                # sign up
                user = MyUser.objects.create_user(phone=phone, is_Doctor=form.cleaned_data['is_Doctor'])
                user.save()

                # sign in
                user = authenticate(request, phone=phone)
                print(user)
                if user is not None:
                    login(request, user)

                global verify
                verify = True
                return redirect('app:home')
            else:
                messages.error(request, 'کد وارد شده اشتباه است')
    else:
        form = CodePhoneDoctorForm()
    context = {
        'form': form,
    }
    return render(request, 'app/phone/verify-login-phone-doctor.html', context)


@login_required(login_url='/loginPhone/')
def ProfileUpdate(request):
    if request.method == 'POST':
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.Profile)
        print(profile_form)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Update Successfully', 'success')
            return redirect('app:profile')

    else:
        profile_form = ProfileUpdateForm(instance=request.user.Profile)
    context = {'profile_form': profile_form}
    return render(request, 'app/profile/UpdateProfile.html', context)


@login_required(login_url='/loginPhone/')
def profile_view(request):
    profile = Profile.objects.filter(user_id=request.user.id)
    context = {
        'profile': profile
    }
    return render(request, 'app/profile/Profile.html', context)
