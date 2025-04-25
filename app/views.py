from django.shortcuts import render
from .models import MyUser
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import *
import random
from django.http import HttpResponse
import requests
import json
from kavenegar import *
from .zarinpal import *




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
        random_code = random.randint(100000, 999999)
        print(random_code)
        # sms = KavenegarAPI(
        #     "***************")  #
        # params = {
        #     'sender': '2000660110',
        #     'receptor': phone,  # 
        #     'message': f' {random_code} سلام این اولین تست است ',
        # }
        # response = sms.sms_send(params)
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
                return redirect('app:post')
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
        random_code = random.randint(100000, 999999)
        print(random_code)
        # sms = KavenegarAPI(
        #     "***********************")  #
        # params = {
        #     'sender': '2000660110',
        #     'receptor': phone,  # 
        #     'message': f' {random_code} سلام این اولین تست است ',
        # }
        # response = sms.sms_send(params)
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
                        return redirect('app:ProfileUpdate')

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


def postView(request):
    post = Post.objects.all().order_by('created_at')
    context = {
        'post': post
    }
    return render(request, 'app/post.html', context)


def singlePost(request, slug):
    single = get_object_or_404(Post, slug=slug)
    context = {
        'single': single
    }
    return render(request, 'app/singlePost.html', context)

def newsView(request):
    news = News.objects.all().order_by('created_at')
    context = {
        'news': news
    }
    return render(request, 'app/news/news.html', context)


def singleNews(request, slug):
    single = get_object_or_404(News, slug=slug)
    context = {
        'singleNews': singleNews
    }
    return render(request, 'app/news/singleNews.html', context)




def category(requests, slug):
    context = {
        "category": get_object_or_404(Category, slug=slug)
    }
    return render(requests, "app/category.html", context)


@login_required(login_url='/loginPhone/')
def reservationView(request , id):
    if request.method == 'POST':
        post = id 
        user = request.user.id 
        city = request.POST['city']
        address = request.POST['address']
        plate = request.POST['plate']
        name = request.POST['name']
        insurance = request.POST['insurance']

        Reserve.objects.create(post_id = post , user_id = user , city = city , 
                               address = address , plate = plate , name = name , 
                               insurance = insurance , paid=False)
        return redirect('app:home')
    
    reserve = Reserve.objects.filter(user = request.user.id)
    return render(request , 'app/reserve/reservation.html' , {'reserve':reserve})


@login_required(login_url='/loginPhone/')
def showReservation(request):
    if request.user.is_Doctor == True:
        reserv = Reserve.objects.filter(accept = False).order_by('-created_at')
        context = {
            'reserv':reserv
        }
        return render(request , 'app/reserve/show_reservation.html' , context)
    else:
        return redirect('app:postView')


@login_required(login_url='/loginPhone/')
def reservationRequest(request , id):
    if request.user.is_Doctor == True:
        if request.method == 'POST':
            reserve = id
            user = request.user.id
            if Accept.objects.create(reserve_id = reserve , user_id = user):
                Reserve.objects.filter(id = reserve).update(accept = True)
            return HttpResponse('قبول شد')
    else:
        return redirect('app:postView')


@login_required(login_url='/loginPhone/')
def cartView(request):
    global pricee
    pricee = 0
    reserve = Reserve.objects.filter(user = request.user.id , paid = False)
    if Reserve.objects.filter(user = request.user.id , paid = False).exists():
        for reserves in reserve :
            pricee += int(reserves.post.price)
    context  = {
        'reserve':reserve,
        'price':pricee
    }
    return render(request , 'app/cart.html' , context)



@login_required(login_url='/loginPhone/')
def request_payment(request):
    if request.method == 'POST':
        global amount
        amount = request.POST['amount']
        description = request.POST['description']

        if str(pricee) == str(amount):
            data = {
                "merchant_id": settings.MERCHANT,
                "amount": amount,
                "description": description,
                "callback_url": CallbackURL,
            }
            data = json.dumps(data)

            headers = {'content-type': 'application/json', 'content-length': str(len(data))}

            response = requests.post(ZP_API_REQUEST, data=data, headers=headers)

            if response.status_code == 200:
                response = response.json()

                if response["data"]['code'] == 100:
                    url = f"{ZP_API_STARTPAY}{response['data']['authority']}"
                    return redirect(url)

                else:
                    return HttpResponse(str(response['errors']))

            else:
                return HttpResponse("مشکلی پیش آمد.")
        else:
            return redirect('app:cartView')
    return redirect('app:cartView')



@login_required(login_url='/loginPhone/')
def verify(request):
    status = request.GET.get('Status')
    authority = request.GET['Authority']

    if status == "OK":
        data = {
            "merchant_id": settings.MERCHANT,
            "amount": amount,
            "authority": authority
        }
        data = json.dumps(data)

        headers = {'content-type': 'application/json', 'Accept': 'application/json'}

        response = requests.post(ZP_API_VERIFY, data=data, headers=headers)

        if response.status_code == 200:
            response = response.json()
            if response['data']['code'] == 100:
                # put your logic here
                Reserve.objects.filter(user=request.user.id).update(paid = True)
                return HttpResponse("خرید شما با موفقیت انجام شد.")

            elif response['data']['code'] == 101:
                return HttpResponse("این پرداخت قبلا انجام شده است.")

            else:
                return HttpResponse("پرداخت شما ناموفق بود.")

        else:
            return HttpResponse("پرداخت شما ناموفق بود.")

    else:
        return HttpResponse("پرداخت شما ناموفق بود.")