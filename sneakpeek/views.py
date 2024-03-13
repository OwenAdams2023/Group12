from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Category, Product, UserProfile
from .forms import SignUpForm
from django import forms
import json
from cart.cart import Cart 

# Create your views here.

def category_summary(request):
    categorites = Category.objects.all()

    return render(request, 'category_summary.html', {"categories": categorites})



def category(request,foo):
    foo = foo.replace("-",' ')

    try:
        category = Category.objects.get(name=foo)
        products = Product.objects.filter(category=category)
        return render(request, 'category.html', {'products':products, 'category':category})
    
    except:
        messages.success(request ("That category doesn't exist"))
        return redirect ('home')



def product(request,pk):
    products = Product.objects.all()
    return render(request, 'product.html',{'products':product})
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

            user = authenticate(username=username, password=forms.PasswordInput)
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
            # shopping cart 
            current_user = UserProfile.objects.get(user__id = request.user_id)
            saved_cart = current_user.old_cart
            if saved_cart:
                converted_cart = json.loads(saved_cart)
                cart = Cart(request)
                for key,value in converted_cart.items():
                    cart.db_add(product=key, quantity= value)

            messages.success(request, ("You have been logged in"))
            return redirect('home')
        
        else:
            messages.success(request, ("There was an error. Please log in again"))
            return redirect('login')
    else:
        return render(request, 'login.html',{})     

def logout_user(request):
    logout(request)
    messages.success(request, ("You have been logged out"))
    return redirect('home',{})        

def payment_success(request):
    return render(request, "payment_success.html,{}")

