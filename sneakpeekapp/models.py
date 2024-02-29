from django.db import models

# Create your models here.

class User(models.Model):
    firrst_name= models.CharField(max_length =30)
    last_name= models.CharField(max_length=30)
    email = models.EmailField(max_length=50)
    phone_number =  models.PhoneNumberField()
    username = models.CharField()
    password =  models.CharField()

def _str_(self):
    return self.title 


