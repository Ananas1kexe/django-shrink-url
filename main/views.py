from django.shortcuts import render, get_object_or_404, redirect
from .models import Link, User
import string
import random
import secrets
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate, logout, login as auth_login
from django.contrib.auth.decorators import login_required

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
        recovery_code = rec_code()
        if User.objects.filter(username=username).first():
            return render(request, "register.html", {"error": "Username alredy used"})
        
        
        if confirmation != password:
            return render(request, "register.html", {"error": "Password do not match"})
        
        
        hashed_password = make_password(password)
        new_user = User(username=username, password=hashed_password, recovery_code=recovery_code)
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
            
            
        if user_code != user.recovery_code:
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
    recover_cd = user.recovery_code
    
    if request.method == "POST":
        if request.POST.get("action") == "delete":
            confirmation = request.POST.get("confirmation")
            recover_code = request.POST.get("recover_code")

            if recover_code == recover_cd:
                if confirmation == "DELETE":
                    user.delete()
                    logout(request)
                    return redirect("/")
            else:
                error = "Please confirm by typing 'DELETE' to delete your account."
        else:
            new_username = request.POST.get("username")
            password = request.POST.get("password")
            check = request.POST.get("check")
            avatar = request.FILES.get("avatar") 
            
            if new_username:
                if User.objects.exclude(id=user.id).filter(username=new_username).exists():
                    return render(request, "profile.html", {"error": "This name is alredy used"})
                else:
                    user.username = new_username   
            if password:
                if not check_password(check, user.password):
                    return render(request, "profile.html", {"error": "Incorrect password"})        
                
                user.set_password(password)
            if avatar:
                user.avatar = avatar
            user.save()
            
            if password:
                user = authenticate(username=user.username, password=password)
                auth_login(request, user)
            return render(request, "profile.html", {"user": user})
            
    return render(request, "profile.html", {"user": user, "links": links, "error": error})

def logouts(request): #робит
    logout(request)
    return redirect("/")
