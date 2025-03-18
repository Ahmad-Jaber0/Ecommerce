from django.db import models
from django.contrib.auth.models import User

class Category(models.TextChoices):
    COMPUTERS='computer'
    Food='food'
    KIDS='kids'
    HOME='home'


class Product(models.Model):
    name=models.CharField(max_length=200,blank=False)
    description=models.TextField(max_length=1000,blank=False)
    price=models.DecimalField(max_digits=7,decimal_places=2,default=0.00)
    brand=models.CharField(max_length=200,blank=False)
    category=models.CharField(max_length=40,blank=False,choices= Category.choices)
    rating=models.DecimalField(max_digits=3,decimal_places=2,default=0)
    stock=models.IntegerField(default=0)
    createdAt=models.DateTimeField(auto_now_add=True)
    user=models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name

