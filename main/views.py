import os
import string
import random
import secrets
from cryptography.fernet import Fernet
from .models import Link, User
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate, logout, login as auth_login
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages

KEY_PATH = os.path.join(settings.BASE_DIR, "secret.key")

if not os.path.exists(KEY_PATH):
    with open(KEY_PATH, "wb") as f:
        f.write(Fernet.generate_key())

with open(KEY_PATH, "rb") as f:
    fernet = Fernet(f.read())
    
    
def encrypt_data(data: str) -> str:
    return fernet.encrypt(data.encode()).decode()

def decrypt_data(token: str) -> str:
    return fernet.decrypt(token.encode()).decode()

def generate_link(lenght=6):
    return "".join(random.choices(string.ascii_letters + string.digits, k=lenght))


def rec_code(lenght=6):
    alphaber = string.ascii_lowercase + string.digits + string.punctuation
    return "".join(secrets.choice(alphaber) for _ in range(lenght))

# Create your views here.
def index(request):
    if request.method == "POST":
        link = request.POST.get("url")
        short_link_id = generate_link()
        new_link = Link.objects.create(user= request.user, link=link, short_id=short_link_id)
        new_link.save()
        return render(request, "index.html", {"new_link": new_link})
    
    return render(request, "index.html", {"new_link": None})

def redirect_to_original(request, pk):
    link = get_object_or_404(Link, short_id=pk)
    return redirect(link.link)



def login(request):#робит
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        
        user = User.objects.filter(username=username).first()

        if user and  check_password(password, user.password):
            auth_login(request, user)
            return redirect("index")
        
        else:
            return render(request, "login.html", {"error": "Not corect username or password"})
        
         
    return render(request, "login.html")

def register(request):#робит
    
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirmation = request.POST.get("confirmation")
        secret_word = request.POST.get("secret_word")
        recovery_code = rec_code()
        if User.objects.filter(username=username).first():
            return render(request, "register.html", {"error": "Username alredy used"})
        
        
        if confirmation != password:
            return render(request, "register.html", {"error": "Password do not match"})
        
        
        hashed_password = make_password(password)


        new_user = User(username=username, password=hashed_password, recovery_code=encrypt_data(recovery_code), secret_word=encrypt_data(secret_word))
        new_user.save()
        
        auth_login(request, new_user)
        return redirect("index")
    return render(request, "register.html")



def recover(request):
    if request.method == "POST":
        username = request.POST.get("username")
        new_password = request.POST.get("new_password")
        confirm_password  = request.POST.get("confirm_password")
        user_code = request.POST.get("user_code")
        
        user = User.objects.filter(username=username).first()
        if user is None:
            return render(request, "recover.html", {"error": "User not found"})
            
            
        if user_code != check_password(user.recovery_code):
            return render(request, "recover.html", {"error": "Code not corect"})



        if confirm_password != new_password:
            return render(request, "recover.html", {"error": "Confirm Password != password"})
        
        user.set_password(new_password)
        user.save()
        return render(request, "recover.html")


    return render(request, "recover.html")


@login_required(login_url="/login")
def profile(request):
    user = request.user
    error = None
    links = user.links.all()
    recovery_code = decrypt_data(user.recovery_code) if user.recovery_code else None
    
    if request.method == "POST":
        if request.POST.get("action") == "delete":
            password = request.POST.get("password")
            if not check_password(password, user.password):
                messages.error(request, "Please enter your password to confirm.")
                return render(request, "profile.html")        
                
            else:
                user.delete()
                logout(request)
                return redirect("/")
        else:
            username = request.POST.get("username")
            password = request.POST.get("password")
            check = request.POST.get("check")
            avatar = request.FILES.get("avatar") 

            if username:
                if User.objects.exclude(id=user.id).filter(username=username).exists():
                    return render(request, "profile.html", {"error": "This name is alredy used", "recovery_code": recovery_code})
                else:
                    user.username = username   
            if password:
                if not check_password(check, user.password):
                    return render(request, "profile.html", {"error": "Incorrect password", "recovery_code": recovery_code})        
                
                user.set_password(password)
            if avatar:
                user.avatar = avatar
            user.save()
            
            if password:
                user = authenticate(username=user.username, password=password)
                auth_login(request, user)
            return render(request, "profile.html", {"user": user, "recovery_code": recovery_code})
    return render(request, "profile.html", {"user": user, "links": links, "error": error, "recovery_code": recovery_code})

def logouts(request): #робит
    logout(request)
    return redirect("/")
