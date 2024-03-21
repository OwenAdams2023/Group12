from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, ProductForm, ShippingAddressForm, ReturnForm #OrderForm
from django import forms
from .models import UserProfile, Category, Product, Order, OrderItem
import json
from cart.cart import Cart
from django.db.models import Q

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

    if request.method == "POST":
        searched = request.POST['searched']
        # seach regardless of case
        searched = Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched))
        if not searched:
             messages.success(request, ("Your item can not be found... Please Try Again "))
             return render(request, "search.html",{})
        return render(request, "search.html",{'searched':searched})
    else:
        return render(request, "search.html",{})

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
            
            current_user = UserProfile.objects.get(user__id = request.user.id)
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

#need to work on checkout
def checkout(request):
    
    #current_user_id = UserProfile.objects.get(user__id = request.user.id)

    #get cart info to send to frontend
    cart = Cart(request)
    cart_products = cart.get_prods()
    quantities = cart.get_quants()
    totals = cart.cart_total()

    if request.method == "POST": 

        user = request.user
        shipping_full_name = request.POST['s_full_name']
        email = request.POST['email']
        amount_paid = totals
        shipping_address = request.POST['shipping_address']
        billing_full_name = request.POST['s_full_name']
        billing_address = request.POST['billing_address']
        card_number = request.POST['card-number']

        #save to order model 
        order = Order.objects.create(
            customer=user,
            shipping_full_name=shipping_full_name,
            email=email,
            amount_paid=amount_paid,
            shipping_address=shipping_address,
            billing_full_name=billing_full_name,
            billing_address=billing_address,
            card_number=card_number
        )

        order.save()

        #save to orderitem model

        for product in cart_products:
            product_id = product.id
            for prod_id, quantity in quantities.items():
                if int(prod_id) == product_id:

                    orderitem = OrderItem.objects.create(
                        order=order,
                        product=product,
                        customer=user,
                        quantity=quantity,
                        price=product.price
                    )
                    orderitem.save()

        messages.success(request, ("Successfully checked out"))
        cart.clear_cart()
        return render(request, "cart_summary.html")

        """order_form = OrderForm(request.POST)
        address_form = ShippingAddressForm(request.POST)
        if order_form.is_valid() and address_form.is_valid():
            order = order_form.save(commit=False)
            order.customer = current_user
            order.save()
            address = address_form.save(commit=False)
            address_form.user = current_user
            address.save()

            order.products.add(*cart)
            request.session['cart']= []
            return redirect('order_success')
        else:
            order_form = OrderForm(initial={'products':cart_items})
            address_form = ShippingAddressForm()
            return render(request, "checkout.html", {'order_form': order_form, 'address_form': address_form})"""

    return render(request, "checkout.html", {"cart_products": cart_products, "quantities":quantities, "totals":totals })


def payment_success(request):
    return render(request, "payment_success.html,{}")

def return_request(request, order_id):
    order= Order.objects.get(id=order_id)
    if request.method == 'POST':
        form = ReturnForm(request.POST)
        if form.is_valid():
            return_request = form.save(commit=False)
            return_request.order = order
            return_request.save()
            return redirect('return_request_success')
        else:
            form = ReturnForm()
        return render(request, 'return_request.html',{'form':form, 'order':order})

def return_request_success(request):
    return render(request, 'return_request_success.html')

