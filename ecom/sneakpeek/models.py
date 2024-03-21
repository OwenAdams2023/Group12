from django.db import models
import datetime
from django.contrib.auth.models import User 
from django.db.models.signals import post_save

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_modified = models.DateTimeField(auto_now=True)
    account_type = models.CharField(max_length=50, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    address1 = models.CharField(max_length=200, blank=True)
    address2 = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=50, blank=True)
    state = models.CharField(max_length=50, blank=True)
    zipcode = models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length=50, blank=True)
    earning = models.DecimalField(default=0, decimal_places=2, max_digits=10)
    old_cart= models.CharField(max_length=200, blank=True,null=True)

    def __str__(self):
        return self.user.username

# Create user account by default when user signs up
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = UserProfile(user=instance)
        user_profile.save()

# Automate profile saving with every instance of User Created
post_save.connect(create_profile, sender=User)

#might not need this
class Account(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    account_type = models.CharField(max_length=20, choices=(('buyer', 'Buyer'), ('seller', 'Seller')), blank=True, null=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}' 

class Category(models.Model):
    product_type = models.CharField(max_length=50)

    def __str__(self):
        return self.product_type

    class Meta:
        verbose_name_plural = 'categories'

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(default=0, decimal_places=2, max_digits=6)
    quantity = models.IntegerField(default=1)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    brand = models.CharField(max_length=100, null=True)
    description = models.CharField(max_length=250, default='', blank=True, null=True)
    image = models.ImageField(upload_to='uploads/product/')
    
    #sale stuff
    #is_sale = models.BooleanField(default=False)
    #sale_price= models.DecimalField(default=0,decimal_places=2,max_digits=6)

    def __str__(self):
        return self.name

class Order(models.Model):
    #product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    shipping_full_name = models.CharField(max_length=250, null=True, blank=True)
    email = models.EmailField(max_length=50, null=True, blank=True)
    date_ordered = models.DateField(auto_now_add=True, null=True, blank=True)
    amount_paid = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    shipping_address = models.TextField(max_length=2000, default='', blank=True)
    billing_full_name = models.CharField(max_length=250, null=True, blank=True)
    billing_address = models.TextField(max_length=2000, default='', blank=True)
    card_number = models.CharField(max_length = 16, default='', blank=True)
    
    def __str__(self):
        return f'Order - {str(self.id)}'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    seller_id = models.IntegerField(default=1)
    quantity = models.PositiveBigIntegerField(default=1)
    price = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self):
        return f'OrderItem - {str(self.id)}'


class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, null=True, blank=True)
    shipping_full_name = models.CharField(max_length= 255)
    shipping_email = models.CharField(max_length= 255)
    shipping_address1 = models.CharField(max_length= 255)
    shipping_address2 = models.CharField(max_length= 255, null=True, blank=True)
    shipping_city = models.CharField(max_length= 255)
    shipping_state = models.CharField(max_length= 255, null=True, blank=True)
    shipping_zipcode = models.CharField(max_length= 255, null=True, blank=True)
    shipping_country = models.CharField(max_length= 255)
    
    class Meta:
        verbose_name_plural = "Shipping Address"
    
    def __str__self(self):
        return f'Shipping Adress - {str(self.id)}'

class ReturnRequest(models.Model):
    order = models.ForeignKey(OrderItem, on_delete=models.CASCADE)
    reason = models.TextField(max_length=500)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Return Request for Order {self.order.id}'

