from rest_framework import serializers

from .models import Cart, Order
        

class CartSerializer(serializers.ModelSerializer):
    cart_food_detail = serializers.ReadOnlyField()
    
    class Meta:
        model = Cart
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    
    
    class Meta:
        model = Order
        fields = '__all__'
        