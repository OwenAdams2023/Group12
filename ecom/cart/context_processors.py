from .cart import Cart

#context processor to make sure cart works on all pages in the site
def cart(request):
    return {'cart': Cart(request)}