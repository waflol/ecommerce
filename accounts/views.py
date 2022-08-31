import email
from email import message
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from core.models import *
# Create your views here.
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('/')
        messages.info(request,'Login Failed, Please Try Again!')
    return render(request,'accounts/login.html')

def user_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        re_password = request.POST.get('re_password')
        phone = request.POST.get('phone')
        if password == re_password:
            if User.objects.filter(username = username).exists():
                messages.info(request,'Username already existed!')
                return redirect('user_register')
            elif User.objects.filter(email = email).exists():
                messages.info(request,'Email already existed!')
                return redirect('user_register')
            else:
                user = User.objects.create_user(username=username,email=email,password=password)
                user.save()
                data = Customer(user=user,phone_field = phone)
                data.save()
                
                # Code for login of user after registering
                auth_user = authenticate(username = username,password=password)
                if auth_user is not None:
                    login(request,auth_user)
                    return redirect('/')
        else:
            messages.info(request,'Password and Confirm Password Missmatch!')
            return redirect('user_register')
    return render(request,'accounts/register.html')

def user_logout(request):
    logout(request)
    return redirect('/')