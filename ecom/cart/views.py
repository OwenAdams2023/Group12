from django.shortcuts import render, get_object_or_404
from .cart import Cart
from sneakpeek.models import Product
from django.http import JsonResponse
from django.contrib import messages


# Create your views here.

def cart_summary(request):
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()
    return render(request, "cart_summary.html",{"cart_products": cart_products, "quantities":quantities, "totals":totals })

    #return render(request, "cart_summary.html")


def cart_add(request):
    cart = Cart(request)

    #this will need the js code added to the product page to send a request when add to cart is pressed
    #https://youtu.be/4NqAiqdjMI8?si=7OstAh7QL_skymNr
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))

        #get product in DB based on product id
        product = get_object_or_404(Product,id=product_id)
        cart.add(product=product, quantity= product_qty)
        cart_quantity = cart.__len__()

        #response= JsonResponse({'Product Name:' : product.name})
        response= JsonResponse({'qty:' : cart_quantity})
        messages.success(request ("Product added to cart"))
        return response

    #return render(request, "cart_add.html")

def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))

        cart.delete(product=product_id )

        response = JsonResponse({'product': product_id})
        messages.success(request ("Product removed from shopping cart"))
        return response


def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))

        cart.update(product= product_id, quantity= product_qty )
        
        response = JsonResponse({'qty': product_qty})
        messages.success(request ("Shopping Cart has been updated"))
        return response
        #return redirect('cart_summary')"""