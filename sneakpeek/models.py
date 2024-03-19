from django.db import models
import datetime
from django.contrib.auth.models import User 
from django.db.models.signals import post_save

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_modified = models.DateTimeField(User, auto_now=True)
    phone = models.CharField(max_length=50, blank=True)
    address1 = models.CharField(max_length=200, blank=True)
    address2 = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=50, blank=True)
    state = models.CharField(max_length=50, blank=True)
    zipcode = models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length=50, blank=True)
    old_cart= models.CharField(max_length=50, blank=True,null=True)

    def __str__(self):
        return self.user.username


# Create user account by default when user signs up
def create_profile(sender, instance, created, **kwards):
    if created:
        user_profile = UserProfile(user=instance)
        user_profile.save()

# Automate profile saving with every instance of User Created
post_save.connect(create_profile, sender=User)

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


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(default=0, decimal_places=2, max_digits=6)
    Category = models.ForeignKey('sneakpeek.Category', on_delete=models.CASCADE, default=1)
    description = models.CharField(max_length=250, default='', blank=True, null=True)
    image = models.ImageField(upload_to='uploads/product/')
    is_sale = models.BooleanField(default=False)
    sale_price= models.DecimalField(default=0,decimal_places=2,max_digits=6)

    def __str__(self):
        return self.name

class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Account, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    address = models.CharField(max_length=100, default='', blank=True)
    phone = models.CharField(max_length=20, default='', blank=True)
    date = models.DateField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)
    card_number = models.CharField(max_length = 16, default='', balnk=True)
    cvv = models.CharField(max_length = 3, default='', balnk=True)
    expiration = models.CharField(max_length = 6, default='', balnk=True)


    def __str__(self):
        return self.product

class Category(models.Model):
    name = models.CharField(max_length=50)

    def _str_(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'categories'

class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length= 255)
    email = models.CharField(max_length= 255)
    address1 = models.CharField(max_length= 255)
    address2 = models.CharField(max_length= 255)
    city = models.CharField(max_length= 255)
    state = models.CharField(max_length= 255, null=True, blank=True)
    zipcode = models.CharField(max_length= 255, null=True, blank=True)
    country = models.CharField(max_length= 255)
    
    class Meta:
        verbose_name_plural = "Shipping Address"
    
    def __str__self(self):
        return f'Shipping Adress - {str(self.id)}'


class ReturnRequest(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Return Request for Order {self.order.id}'
