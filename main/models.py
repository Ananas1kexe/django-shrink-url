from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.

class Link(models.Model):
    link = models.CharField("link", max_length=55)
    short_id = models.CharField("short_id", max_length=10, unique=True)
    
class UserManager(BaseUserManager):
    def create_user(self, username, password = None, **extra_fields):
        if not username:
            raise ValueError("the username field must be set")
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_super_user(self, username, password = None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        
        return self.create_user(username, password, **extra_fields)



class User(AbstractBaseUser):
    username = models.CharField("username", unique=True, max_length=50)
    password = models.CharField("password", max_length=255)
    avatar = models.ImageField("avatar", blank=True)
    blok = models.BooleanField("block" ,default=False)
    recovery_code = models.CharField("recovery_code")
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()
    
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []
    
    def __str__(self):
        return self.username
    
    def has_perm(self, perm, obj=None):
        return self.is_superuser
    
    def has_module_perms(self, app_label):
        return self.is_superuser