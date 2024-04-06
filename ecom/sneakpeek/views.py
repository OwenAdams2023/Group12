from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, ProductForm, ShippingAddressForm, ReturnForm, UpdateUserForm, UpdatePasswordForm, UpdateUserInfoForm, UpdateProductInfoForm
from django import forms
from .models import UserProfile, Category, Product, Order, OrderItem, ReturnRequest
import json
from django.http import JsonResponse
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
            #user.userprofile.earning = 0
            user.userprofile.save()
            
            messages.success(request, ("Your account creation has been sent for approval."))
            return redirect('home')

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
            user_approved = user.userprofile.approved

            if user_approved==True:
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

            elif user_approved==None:
                messages.success(request, ("Unable to log in...."))
                messages.success(request, ("You account is still pending approval!"))

            else:
                messages.success(request, ("Unable to log in...."))
                messages.success(request, ("You account creation was rejected!"))
        
        else:
            messages.success(request, ("Wrong credentials. Please try again"))
            return redirect('login')
        
    return render(request, 'login.html', {})     

def logout_user(request):
    logout(request)
    messages.success(request, ("You have been logged out"))
    return redirect('home') 

def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user

        # filling in the password
        if request.method == 'POST':
            form = UpdatePasswordForm(current_user, request.POST)
            # check for validity
            if form.is_valid():
                form.save()
                messages.success(request, "Password Updated ")
                login(request, current_user)
                return redirect('update_user')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                    return redirect('update_password')
        else:
            form = UpdatePasswordForm(current_user)
            return render(request, "update_password.html", {'user_form':form})
    else: 
        messages.success(request, "You must be logged in")
        return redirect('home')

    #return render(request, "update_password.html", {'user_form':form})

def update_info(request):
    if request.user.is_authenticated:
        current_user = UserProfile.objects.get(user__id=request.user.id)
        form = UpdateUserInfoForm(request.POST or None, instance=current_user)

        if form.is_valid():
            form.save()
            messages.success(request, "Your information has been updated!")
            return redirect('home')
        return render(request, "update_info.html", {'form':form})

    else:
         messages.success(request, "Please log in first before updating your account")
         return redirect('home')


def update_user(request):

    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)
        #password_form = UpdatePasswordForm(current_user, request.POST)

        if user_form.is_valid():
            user_form.save()

            login(request,current_user)
            messages.success(request, "Your information has been updated!")
            return redirect('home')

    else:
        messages.success(request, "Please log in first before updating your account")
        return redirect('home')

    return render(request, "update_user.html", {'user_form':user_form})
   

def product(request,pk):
    product = Product.objects.get(id=pk)
    #products = Product.objects.all()
    return render(request, 'product.html',{'product':product})

def update_earning(request):

    current_seller = request.user
    sold_orders = OrderItem.objects.filter(seller_id=current_seller.id)

    if request.method == "POST":
        current_user = request.user
        current_user.userprofile.earning = 0
        current_user.userprofile.save()

        messages.success(request, "We have initiated the transfer")

    return render(request, 'seller_earnings.html', {'sold_orders':sold_orders})

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

    current_user = request.user
    if current_user.is_authenticated:
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
                        seller_id=product.seller.id

                        orderitem = OrderItem.objects.create(
                            order=order,
                            product=product,
                            customer=user,
                            seller_id=seller_id,
                            quantity=quantity,
                            price=product.price
                        )
                        orderitem.save()

                        #deal with managing product on database
                        product = Product.objects.get(pk=product_id)
                        curr_qty = product.quantity

                        product.quantity = curr_qty - quantity  #delete items from database
                        if (product.quantity == 0):
                            product.delete()

                        product.save()

                        #add earning to the seller's account
                        seller = User.objects.get(pk=seller_id)
                        curr_earning = seller.userprofile.earning
                        seller.userprofile.earning = curr_earning + (product.price * quantity)
                        seller.userprofile.save()


            messages.success(request, ("Successfully checked out"))
            cart.clear_cart()
            return render(request, "PaymentSuccess.html")

    else:
        messages.success(request, ("Please log in to Checkout"))
        return redirect('login')

    return render(request, "checkout.html", {"cart_products": cart_products, "quantities":quantities, "totals":totals })

def order_history(request):

    current_user = request.user
    user_orders = OrderItem.objects.filter(customer=current_user)

    return render(request, "order_history.html", {'user_orders': user_orders})

def product_list(request):

    current_user = request.user
    user_products = Product.objects.filter(seller=current_user)

    return render(request, "product_list.html", {'user_products': user_products})

def product_delete(request):

    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product= Product.objects.get(pk=product_id)

        product.delete()

        response = JsonResponse({'product': product_id})
        messages.success(request, ("Product listing removed from the site"))
        return response

def product_update(request,pk):

    product= Product.objects.get(pk=pk)
    form = UpdateProductInfoForm(request.POST or None, instance=product)

    if request.method == 'POST':

        if form.is_valid():
            form.save()
            messages.success(request, "Your information has been updated!")
    
    return render(request, "update_product_info.html", {'form':form, 'product':product})
    
    #return render(request, "update_product_info.html", {'form':form})

    #return render(request, "update_product_info.html", {'form': form, 'product':product})


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

#admin actions
def account_approval(request):

    pending_accounts = User.objects.filter(userprofile__approved__isnull=True).order_by('date_joined')

    return render(request, 'pending_account_approval.html', {'accounts':pending_accounts})

def account_action(request):

    if request.POST.get('action') == 'post':
        user_id = int(request.POST.get('user_id'))
        admin_action = request.POST.get('admin_action')

        user= User.objects.get(pk=user_id)

        if admin_action == "reject":
            user.userprofile.approved = False
            response = JsonResponse({'user': user_id})
            messages.success(request, ("User profile creation has been rejected. User has been removed."))

        elif admin_action == "approve":
            user.userprofile.approved = True
            response = JsonResponse({'user': user_id})
            messages.success(request, ("User profile creation has been approved"))

        user.userprofile.save()
        return response

