

from django.urls import path
from . import views
urlpatterns = [
    path("", views.index, name="index"),
    path("<str:pk>", views.redirect_to_original, name="redirect"),
    
    path("login/", views.login, name="login"),
    path("register/", views.register, name="register"),
    
    path("recover/", views.recover, name="recover"),
    path("profile/", views.profile, name="profile"),
    path("settings/", views.settings, name="settings"),

]
