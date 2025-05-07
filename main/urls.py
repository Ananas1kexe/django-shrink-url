

from django.urls import path
from . import views
urlpatterns = [
    path("", views.index, name="index"),    
    path("login/", views.login, name="login"),
    path("register/", views.register, name="register"),
    path("logout/", views.logouts, name="logout"),
    path("recover/", views.recover, name="recover"),
    path("profile/", views.profile, name="profile"),

    path("<str:pk>/", views.redirect_to_original, name="redirect"),


]
