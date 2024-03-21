from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, ProductForm, ShippingAddressForm, ReturnForm #OrderForm
from django import forms
from .models import UserProfile, Category, Product, Order, OrderItem, ReturnRequest
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
        password = request.POST['password1']
        account_type = request.POST['account_type']

        first_name = request.POST['first_name'] # can also use request.POST['first_name']
        last_name = request.POST['last_name']

        try:
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

        except:
            messages.success(request, ("Account with those creddentials already exist. Try again"))
            return redirect('register')

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
            messages.success(request, ("Wrong credentials. Please try again"))
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

        for product in cart_products:
            product_id = product.id
            for prod_id, quantity in quantities.items():
                if int(prod_id) == product_id:
                    
                    product = Product.objects.get(pk=product_id)
                    warehouse_qty = product.quantity
                    if (warehouse_qty < quantity):
                        messages.success(request, ("There isn't enough product at the warehouse at the moment. Please try again"))
                        return redirect('cart_summary')

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

                    product = Product.objects.get(pk=product_id)
                    curr_qty = product.quantity

                    product.quantity = curr_qty - quantity  #delete items from database
                    if (product.quantity == 0):
                        product.delete()


        messages.success(request, ("Successfully checked out"))
        cart.clear_cart()
        return render(request, "cart_summary.html")

    return render(request, "checkout.html", {"cart_products": cart_products, "quantities":quantities, "totals":totals })

def order_history(request):

    current_user = request.user
    user_orders = OrderItem.objects.filter(customer=current_user)

    return render(request, "order_history.html", {'user_orders': user_orders})

def payment_success(request):
    return render(request, "payment_success.html,{}")

def return_request(request, order_id):
    order= OrderItem.objects.get(id=order_id)

    if request.method == 'POST':
        reason = request.POST['reason']
        return_request = ReturnRequest.objects.create(
            order=order,
            reason=reason
        )

        return_request.save()
        messages.success(request, ("Order Return has been initiated"))
        return render(request, 'return_request_successful.html')

    return render(request, 'returnRequest.html', {'order':order})

def return_request_success(request):
    return render(request, 'return_request_success.html')

