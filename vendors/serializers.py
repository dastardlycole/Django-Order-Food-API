from rest_framework import serializers

from .models import Menu, Food


class FoodSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Food
        fields = '__all__'
        
        

class MenuSerializer(serializers.ModelSerializer):
    food_detail = serializers.ReadOnlyField()
    
    class Meta:
        model = Menu
        fields = '__all__'
        