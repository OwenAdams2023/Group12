from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm
from django import forms

# Create your views here.
def home(request):
    return render(request, "home.html")

def register_user(request):

    form = SignUpForm()

    if request.method == "POST":       # get info when the user enters it and presses submit from register.html file
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            user = authenticate(username=username, password=password1)
            login(request, user)
            messages.success(request ("Your registration is complete"))
            return redirect('home')

        else:
            messages.success(request ("There was a problem. Please try again"))
        """
        account_type = request.POST['account_type']
        first_name = request.POST['first_name']  
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone_number = request.POST['phone_number']
        username = request.POST['username']
        passw1 = request.POST['passw']
        passw2 = request.POST['verify_passw']
        """

        return redirect('login_user')

    return render(request, 'register.html')

def login_user(request):

    if request.method == "POST": 
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ("You have been logged in"))
            return redirect('home')
        
        else:
            messages.success(request, ("There was an error. Please log in again"))
            return redirect('login')
        
    return render(request, 'login.html')     

def logout_user(request):
    logout(request)
    messages.success(request, ("You have been logged out"))
    return redirect('home')        