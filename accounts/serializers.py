from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=255, write_only = True)
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'password', 'is_vendor', 'is_customer']