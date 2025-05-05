from django.db import models

# Create your models here.

class Link(models.Model):
    link = models.CharField("link", max_length=55)
    short_id = models.CharField("short_id", max_length=10, unique=True)
    
    