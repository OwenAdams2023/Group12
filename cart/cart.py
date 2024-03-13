from sneakpeek.models import Product, UserProfile
class Cart():
    def __init__(self,request):
        self.session = request.session

        self.request = request

        cart = self.session.get('session_key')

        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}
        

        self.cart = cart
def db_add(self,product,quantity):
    product_id = str(product)
    product_qty = str(quantity)

    if product_id in self.cart:
        pass
    else:
        #self.cart[product_id]= {'price': str(product.price)}
        self.cart[product_id]= int(product_qty)

    self.session.modified = True

    # logged in user 
    if self.request.user.is_authenticated:
        current_user = UserProfile.objects.filter(user__id=self.request.user.id)


        cart_string = str(self.cart)
        cart_string = cart_string.replace ("\'", "\"")

        current_user.update(pld_cart= str(cart_string))

def add(self,product,quantity):
    product_id = str(product.id)
    product_qty = str(quantity)

    if product_id in self.cart:
        pass
    else:
        #self.cart[product_id]= {'price': str(product.price)}
        self.cart[product_id]= int(product_qty)

    self.session.modified = True

    # logged in user 
    if self.request.user.is_authenticated:
        current_user = UserProfile.objects.filter(user__id=self.request.user.id)


        cart_string = str(self.cart)
        cart_string = cart_string.replace ("\'", "\"")

        current_user.update(pld_cart= str(cart_string))






def __len__(self):
    return len(self.cart)

def get_prods(self):
    product_ids = self.cart.keys()
    products= Product.objects.filter(id__in= product_ids)
    return products

def get_quants(self):
    quantities = self.cart
    return quantities

def update(self,product,quantity):
    product_id = str(product)
    product_qty = int(quantity)

    ourcart = self.cart
    ourcart[product_id]= product_qty

    self.session.modified = True

    thing =self.cart
    
    if self.request.user.is_authenticated:
        current_user = UserProfile.objects.filter(user__id=self.request.user.id)


        cart_string = str(self.cart)
        cart_string = cart_string.replace ("\'", "\"")

        current_user.update(pld_cart= str(cart_string))

    return thing 

def delete(self,product):
    product_id= str(product)

    if product_id in self.cart:
        del self.cart[product_id]
    
    self. session.modified = True
    if self.request.user.is_authenticated:
        current_user = UserProfile.objects.filter(user__id=self.request.user.id)


        cart_string = str(self.cart)
        cart_string = cart_string.replace ("\'", "\"")

        current_user.update(pld_cart= str(cart_string))


def total(self):
    product_ids = self.cart.keys()

    products = Product.objects.filter(id__in=product_ids)

    quantities = self.cart

    total = 0
    for key, value in quantities.items():

        key = int(key)

        for product in products: 
            if product.id == key:
                if product.is_sale:
                    total = total + (product.sale_price *value)
                else: 
                    total = total + (product.price *value)
                
    return total 
