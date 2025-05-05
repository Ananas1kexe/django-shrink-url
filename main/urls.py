

from django.urls import path
from . import views
urlpatterns = [
    path("", views.index, name="index"),
    path("<str:pk>", views.redirect_to_original, name="redirect"),
]
