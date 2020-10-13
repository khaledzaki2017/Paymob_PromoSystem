from django.db import models
from django.contrib.auth.models import User


class User(User):
    username = models.CharField(max_length=100, null=True, blank=True)
    useraddress = models.CharField(max_length=200, null=True, blank=True)
    mobile_number = models.CharField(max_length=30, null=True, blank=True)
    is_admin = models.BooleanField(default=False)


class Promo(models.Model):

    
    user = models.ForeignKey(User, null=True,  on_delete=models.CASCADE)
    description = models.TextField()
    is_active = models.BooleanField(default=False)

    _type = models.CharField(max_length=100)
    _code = models.CharField(max_length=100, unique=True)
    _amount = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    
    
    class Meta:
        ordering = ('-created_at',)