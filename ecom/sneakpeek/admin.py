from django.contrib import admin
from .models import Category, Product, Order, OrderItem, UserProfile, ReturnRequest, Size
from django.contrib.auth.models import User


# Register your models here.
admin.site.register(Category)
admin.site.register(Size)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(UserProfile)
admin.site.register(ReturnRequest)

class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "quantity", "seller", "brand")
admin.site.register(Product, ProductAdmin)

#Mix profile info and user info
class ProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    fk_name = 'user'

class UserAdmin(admin.ModelAdmin):
    model = User
    field = ("username", "first_name", "last_name", "email")
    inlines = (ProfileInline, )
    list_display = ("username", "first_name", "last_name", "email", "is_staff")
    #list_select_related = ('userprofile', )

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
