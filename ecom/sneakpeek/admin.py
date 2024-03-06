from django.contrib import admin
from .models import Category, Account, Product, Order, UserProfile
from django.contrib.auth.models import User


# Register your models here.
admin.site.register(Category)
admin.site.register(Account)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(UserProfile)

#Mix profile info and user info
class ProfileInline(admin.StackedInline):
    model = UserProfile

class UserAdmin(admin.ModelAdmin):
    model = User
    field = ["username", "first_name", "last_name", "email"]
    inlines = [ProfileInline]

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
