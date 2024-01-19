from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request, "index.html")

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        password2 = request.POST["confirm-password"]

        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, "That username is taken")
                return redirect("register")
            elif User.objects.filter(email=email).exists():
                messages.error(request, "That email is being used")
                return redirect("register")
            else:
                user = User.objects.create_user(
                    username=username, email=email, password=password
                )
                user.save()
                messages.success(request, "Successfully registered you can login")
                return redirect("login")
        else:
            messages.error(request, "Passwords do not match")
            return redirect("register")
        
    return render(request, "register.html")

def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, "Successfully logged in")
            return redirect("index")
        else:
            messages.error(request, "Invalid credentials")
            return redirect("login")
        
    return render(request, "login.html")

def logout(request):
    auth.logout(request)
    messages.success(request, "Successfully logged out")
    return redirect("index")
    

