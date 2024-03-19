from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, ProductForm
from django import forms
from .models import UserProfile, Category, Product
import json
from cart.cart import Cart

# Create your views here.

#need to make changes to home for adding product list
def home(request):
    
    if request.user.is_authenticated:
        current_user = request.user
        is_seller = current_user.userprofile.account_type == 'Seller'
        #context = {'is_seller': is_seller}
        #return render(request, "home1.html", context)

    else:
        is_seller = False

    products = Product.objects.all()
    #return render(request, 'product.html',{'products':products})

    #return render(request, "home1.html")
    return render(request, "home.html", {'products':products, 'is_seller':is_seller})

def search(request):

    pass

def register_user(request):

    if request.method == "POST":      # get info when the user enters it and presses submit from register.html file
        email = request.POST['email']
        phone_number = request.POST['phone']
        username = request.POST['username']
        password = request.POST['password']
        account_type = request.POST['account_type']

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
            
            #reload the cart
            """
            current_user = UserProfile.objects.get(user__id = request.user_id)
            saved_cart = current_user.old_cart
            if saved_cart:
                converted_cart = json.loads(saved_cart)
                cart = Cart(request)
                for key,value in converted_cart.items():
                    cart.db_add(product=key, quantity= value)"""

            messages.success(request, ("You have been logged in"))
            return redirect('home')
        
        else:
            messages.success(request, ("There was an error. Please log in again"))
            return redirect('login')
        
    return render(request, 'login.html', {})     

def logout_user(request):
    logout(request)
    messages.success(request, ("You have been logged out"))
    return redirect('home')    

def product(request,pk):
    product = Product.objects.get(id=pk)
    #products = Product.objects.all()
    return render(request, 'product.html',{'product':product})

def category(request,cat_name):
    cat_name = cat_name.replace("-",' ')

    try:
        category = Category.objects.get(name=cat_name)
        products = Product.objects.filter(category=category)
        return render(request, 'category.html', {'products':products, 'category':category})
    
    except:
        messages.success(request ("That category doesn't exist"))
        return redirect ('home')

def category_summary(request):
    categorites = Category.objects.all()

    return render(request, 'category_summary.html', {"categories": categories})

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

def payment_success(request):
    return render(request, "payment_success.html,{}")

def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)

        if user_form.is_valid():
            user_form.save()

            login(request,current_user)
            messages.success(request, "Your information has been updated!")
            return redirect('home')
        return render(request, "update_user.html", {'user':user_form})
    
    else:
         messages.success(request, "Please log in first before updating your account")
         return redirect('home')
