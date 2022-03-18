import email
from rest_framework.response import Response
from rest_framework import status 
from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from accounts.serializers import  UserSerializer
from customers.serializers import OrderSerializer
from customers.models import Order, Cart
from vendors.serializers import FoodSerializer
from vendors.models import Food, Menu
from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.auth import authenticate
from django.forms import model_to_dict
from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser

User = get_user_model()

@api_view(['GET'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def user_view(request):
    user=request.user
    if user.is_admin == False:
            raise PermissionDenied(detail={"message":f"Permission Denied. Only admin can perform this action"})
    if request.method == 'GET':
        # Get all the users in the database
        all_users = User.objects.filter(is_active=True)
        
        serializer = UserSerializer(all_users, many=True)
        
        data = {
           "message":"successful",
           "data": serializer.data
        }
    
    
        # return JsonResponse(data)
        return Response(data, status=status.HTTP_200_OK)

# get all orders and delete all orders not necessary only for admin
@api_view(['GET'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def get_orders(request):
    # get all orders
    user= request.user
    if user.is_admin == False:
            raise PermissionDenied(detail={"message":f"Permission Denied. Only admin can perform this action"})
    
    if request.method == "GET":
        order = Order.objects.all()
        serializer = OrderSerializer(order, many=True)
        
        data = {
           "message":"successful",
           "data": serializer.data
        }
    
    
        return Response(data, status=status.HTTP_200_OK)    

@api_view(['DELETE'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def delete_all_orders(request): 
    # delete all orders
    user=request.user  
    if user.is_admin == False:
            raise PermissionDenied(detail={"message":f"Permission Denied. Only admin can perform this action"})
    if request.method == 'DELETE':
        order = Order.objects.all()
        for i in order:
            i.delete()

        return Response({}, status=status.HTTP_204_NO_CONTENT)         
@api_view(['DELETE'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def delete_all_food(request): 
    # delete all food
    user=request.user  
    if user.is_admin == False:
            raise PermissionDenied(detail={"message":f"Permission Denied. Only admin can perform this action"})
    if request.method == 'DELETE':
        food = Food.objects.all()
        for i in food:
            i.delete()

        return Response({}, status=status.HTTP_204_NO_CONTENT)         
@api_view(['DELETE'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def delete_all_carts(request): 
    # delete all carts
    user=request.user  
    if user.is_admin == False:
            raise PermissionDenied(detail={"message":f"Permission Denied. Only admin can perform this action"})
    if request.method == 'DELETE':
        carts = Cart.objects.all()
        for i in carts:
            i.delete()

        return Response({}, status=status.HTTP_204_NO_CONTENT)         
@api_view(['DELETE'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def delete_all_menus(request): 
    # delete all menus
    user=request.user  
    if user.is_admin == False:
            raise PermissionDenied(detail={"message":f"Permission Denied. Only admin can perform this action"})
    if request.method == 'DELETE':
        menus = Menu.objects.all()
        for i in menus:
            i.delete()

        return Response({}, status=status.HTTP_204_NO_CONTENT)         


@api_view(['GET'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def get_food(request):
    user = request.user
    # get all food in the database only for admins
    if request.method == "GET":
        if user.is_admin == False:
            raise PermissionDenied(detail={"message":f"Permission Denied. Only admin can perform this action"})
        food_items = Food.objects.all()
        serializer = FoodSerializer(food_items, many=True)
        
        data = {
           "message":"successful",
           "data": serializer.data
        }
    
    
        return Response(data, status=status.HTTP_200_OK) 
