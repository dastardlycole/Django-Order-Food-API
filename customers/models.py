from django.db import models
from django.contrib.auth import get_user_model
from vendors.models import Food
from django.forms import model_to_dict

User = get_user_model()
# Create your models here.

    
    
    

class Cart(models.Model):
    user       = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="cart")
    food       = models.ForeignKey(Food, on_delete=models.CASCADE, related_name="cart")
    date_added = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self) -> str:
        return self.user
    
    @property
    def cart_food_detail(self):
        return model_to_dict(self.food)

class Order(models.Model):
    user       = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="order")
    choices = (
        ("cash", "Cash"),
        ("card", "Card"),

    )
    address = models.CharField(max_length=1000)
    message = models.CharField(max_length=1000)
    payment_choice = models.CharField(max_length=355, choices=choices, default='cash')
    
    