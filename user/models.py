from django.db import models
from django.contrib.auth.models  import AbstractUser
from .managers import CustomUserManager
# Create your models here.

class User(AbstractUser):
    ROLE_CHOICES=(
        ('admin','Admin'),
        ('staff','Staff'),
        ('customer','Customer'),
        ('delivery', 'Delivery Driver')
        )
    email=models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=False,null=True,blank=True)
    role = models.CharField(max_length=10,choices=ROLE_CHOICES)
    phone_number = models.CharField(max_length=10,blank=True,null=True,unique=False)
    address = models.TextField(blank=True,null=True)
    
    email_otp = models.IntegerField(null=True,blank=True)
    email_otp_created_at = models.DateTimeField(null=True,blank=True)
    is_email_verified = models.BooleanField(default=False)

    
    USERNAME_FIELD="email"
    REQUIRED_FIELDS=[]

    objects=CustomUserManager()

    def __str__(self):
        return self.username