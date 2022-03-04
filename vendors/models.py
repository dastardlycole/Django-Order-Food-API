from django.db import models
from django.contrib.auth import get_user_model
from django.forms import model_to_dict

User = get_user_model()
# Create your models here.


class Food(models.Model):
    Category = (
        ("nigerian", "Nigerian"),
        ("african", "African"),
        ("american", "American"),
        ("asian", "Asian"),
        ("european", "European"),
        ("italian", "Italian"),
        ("other", "Other"),
    )
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=1000)
    category = models.CharField(max_length=355, choices=Category, default='other')
    price = models.DecimalField(max_digits=11, decimal_places=2, default=0.00)
    user       = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="food")
    date_added = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self) -> str:
        return f"{self.title}"
    
    
    

class Menu(models.Model):
    user       = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="menu")
    food       = models.ForeignKey(Food, on_delete=models.CASCADE, related_name="menu")
    date_added = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self) -> str:
        return self.user
    
    @property
    def food_detail(self):
        return model_to_dict(self.food)