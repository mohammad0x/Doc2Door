from django.shortcuts import render
from .models import MyUser
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import * 

# Create your views here.
def Home(request):
    return render(request , 'app/home.html')

def Login(request):
    if request.user.is_authenticated:
        return redirect('app:home')
    if request.method == 'POST':
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        user = authenticate(request, phone=phone, password=password)
        if user is not None:
            login(request, user)
            return redirect("app:home")
        else:
            context = {
                "phone": phone,
                "errormessage": "User not found"
            }
            return render(request, "app/login.html", context)
    else:
        return render(request, 'app/login.html', {})


def Register(request):
    if request.user.is_authenticated:
        return redirect('app:login')
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        phone = form['phone'].value()
        if MyUser.objects.filter(phone=phone).exists():
            messages.error(request, 'شماره  شما تکراری است.')
            return redirect('app:register')
 
        if form.is_valid():
            data = form.cleaned_data
            user = MyUser.objects.create_user(phone=data['phone'],  password=data['password'])
            user.save()
            return redirect('app:login')
        else:
            messages.error(request, 'Something is wrong! Please try again', 'danger')
    else:
        form = UserCreateForm()
    context = {'form': form}
    return render(request, 'register/register.html')



@login_required(login_url='/login/')
def Logout_view(request):
    logout(request)
    return redirect('app:home')
