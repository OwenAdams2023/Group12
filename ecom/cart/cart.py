from sneakpeek.models import Product, UserProfile

class Cart():
    def __init__(self,request):
        self.session = request.session
        #get request
        self.request = request
        
        #get current session key (returning users)
        cart = self.session.get('session_key')

        #for new users
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}
        
        self.cart = cart

    #add to cart from the saved database
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

            current_user.update(old_cart= str(cart_string))


    def add(self,product): #,quantity):
        product_id = str(product_id)
        #product_qty = str(quantity)

        if product_id in self.cart:
            pass
        else:
            self.cart[product_id]= {'price': str(product.price)}
            #self.cart[product_id]= int(product_qty)

        self.session.modified = True

        # if user logged in
        if self.request.user.is_authenticated:
            current_user = UserProfile.objects.filter(user__id=self.request.user.id)

            #get cart info of current user
            cart_string = str(self.cart)
            #convert the current dict string into db dict 
            cart_string = cart_string.replace ("\'", "\"")

            #save the cart string to userprofile
            current_user.update(old_cart= str(cart_string))



    def __len__(self):
        return len(self.cart)

    def get_prods(self):
        product_ids = self.cart.keys()

        #look up product in DB using product id
        products= Product.objects.filter(id__in= product_ids)
        return products

    def get_quants(self):
        quantities = self.cart
        return quantities

    def update(self,product,quantity):
        product_id = str(product)
        product_qty = int(quantity)

        #get cart and update quantity for product id
        ourcart = self.cart
        ourcart[product_id]= product_qty

        self.session.modified = True

        thing =self.cart
        
        #if user is logged in, update cart info on database
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
        
        self.session.modified = True

        #if user logged in, update cart info on database
        if self.request.user.is_authenticated:
            current_user = UserProfile.objects.filter(user__id=self.request.user.id)
            cart_string = str(self.cart)
            cart_string = cart_string.replace ("\'", "\"")

            current_user.update(pld_cart= str(cart_string))


    def cart_total(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        #get quantity
        quantities = self.cart

        total = 0
        for key, value in quantities.items():

            key = int(key)
            for product in products: 
                if product.id == key:
                    """
                    if product.is_sale:
                        total = total + (product.sale_price *value)
                    else: 
                        total = total + (product.price *value)
                        """
                    total = total + (product.price *value)
                                    
        return total 


