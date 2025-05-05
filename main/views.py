from django.shortcuts import render, get_object_or_404, redirect
from .models import Link
import string
import random


def generate_link(lenght=6):
    return "".join(random.choices(string.ascii_letters + string.digits, k=lenght))



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