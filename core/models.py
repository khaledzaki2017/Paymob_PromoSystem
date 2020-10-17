from django.db import models
from django.contrib.auth.models import User


class User(User):

    name = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    mobile_number = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        
            return self.name

class Promo(models.Model):

    
    user = models.ForeignKey(User, null=True,  on_delete=models.CASCADE)
    description = models.TextField()
    is_active = models.BooleanField(default=False)

    _type = models.CharField(max_length=100)
    promo = models.CharField(max_length=100, unique=True)
    amount = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now=True)
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    
    
    class Meta:
        ordering = ('-created_at',)