from django.shortcuts import render, get_object_or_404, redirect
from .models import Link
import string
import random
import secrets

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
        new_link = Link(link=link, short_id=short_link_id)
        new_link.save()
        return render(request, "index.html", {"new_link": new_link})
    
    return render(request, "index.html", {"new_link": None})

def redirect_to_original(request, pk):
    link = get_object_or_404(Link, short_id=pk)
    return redirect(link.link)



def login(request):
    return render(request, "login.html")

def register(request):
    return render(request, "register.html")

def recover(request):
    return render(request, "recover.html")

def profile(request):
    return render(request, "profile.html")

def settings(request):
    return render(request, "settings.html")


