from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def home(request):
    return render(request, "sneakpeekapp/index.html")

def register(request):

    if request.method == "POST":                    # get info when the user enters it and presses submit from register.html file
        first_name = request.POST.get('first_name') # can also use request.POST['first_name']
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        username = request.POST.get('username')
        passw = request.POST.get('passw')

        myUser = User.objects.create_user(username, email, passw) #create user object
        myUser.first_name = first_name
        myUser.last_name = last_name
        myUser.phone_number = phone_number

        myUser.save()

        messages.success(request, "Your Account has been succesfully registered and sent for approval.") #display message after saving
        return redirect('login') #redirect to login page after registration


    return render(request, "sneakpeekapp/register.html")

def login(request):
    if request.method == 'POST':
        username= request.POST['username']
        passw = request.POST['passww']

        user= authenticate(username=username, password=passw)
        if user is not None:
            login(request,user)
            first_name= user.first_name
            return redirect('home')
        #if information is incorrect redirect back to the login page 
        else:
            messsage.error(request, "Login information incorrect")
            return redirect('login') 

    return render(request, "sneakpeekapp/login.html")


def logout(request):
    logout(request)
    messages.success(request, "Logged Out")
    return  redirect('home')




