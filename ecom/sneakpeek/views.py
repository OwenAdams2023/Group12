from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, ProductForm
from django import forms
from .models import UserProfile

# Create your views here.
def home(request):

    if request.user.is_authenticated:
        current_user = request.user
        is_seller = current_user.userprofile.account_type == 'Seller'
        context = {'is_seller': is_seller}
        return render(request, "home.html", context)

    return render(request, "home.html")

def register_user(request):

    if request.method == "POST":                    # get info when the user enters it and presses submit from register.html file
        email = request.POST['email']
        phone_number = request.POST['phone']
        username = request.POST['username']
        password = request.POST['password']
        user_type = request.POST['account_type']

        first_name = request.POST['first_name'] # can also use request.POST['first_name']
        last_name = request.POST['last_name']

        user = User.objects.create_user(username, email, password) #create user object
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        #saving phone number
        user.userprofile.phone = phone_number
        user.userprofile.account_type = account_type
        user.userprofile.save()

        user = authenticate(username=username, password=password)
        login(request, user)

        return redirect('login')

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

@login_required
def add_product(request):
    form = ProductForm()
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.seller = request.user
            form.save()
            return redirect('home')

        else:
            form = ProductForm()
        
    return render(request, 'add_product.html', {'form': form})