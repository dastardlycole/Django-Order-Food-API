from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .models import Menu, Food
from .serializers import MenuSerializer, FoodSerializer
from drf_yasg.utils import swagger_auto_schema
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError, PermissionDenied

# Create your views here.
@swagger_auto_schema(methods=['POST'] ,
                    request_body=FoodSerializer())
@api_view(['POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def food_view(request):
    
    # add food to database and vendor's menu
    if request.method == 'POST':
        user=request.user
        if user.is_vendor == False:
            raise PermissionDenied(detail={"message":f"Permission Denied. Only vendors can perform this action"})
        serializer = FoodSerializer(data=request.data)
        if serializer.is_valid(): 
            if "user" in serializer.validated_data.keys():
                serializer.validated_data.pop("user") 
            title = serializer.validated_data['title']    
            description = serializer.validated_data['description']    
            category = serializer.validated_data['category']    
            price = serializer.validated_data['price']       
            check = Food.objects.filter(title=title,description=description,category=category,price=price,user=user)           
            if check.exists():
                raise PermissionDenied(detail={"message":"You already have this item"})
            food = Food.objects.create(title=title,description=description,category=category,price=price,user=user)           
            new_serializer=FoodSerializer(food) 
            
            Menu.objects.create(food=food,user=user)
            data = {
                'message' : 'success',
                'data'  : new_serializer.data,
                'menu id': Menu.objects.get(food=food,user=user).id
            }
            return Response(data, status=status.HTTP_202_ACCEPTED)
        else:
            data = {
                'message' : 'failed',
                'error'  : serializer.errors
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        
    
    
    

    
    
@swagger_auto_schema(methods=['put'] ,
                    request_body=FoodSerializer())
@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def food_detail(request, food_id):

    # get, edit and delete individual food
    try:
        food = Food.objects.get(id=food_id)
    except Food.DoesNotExist:

        data = {
            'message' : 'failed',
            'error'  : f"Food item with ID {food_id} does not exist."
        }
        return Response(data, status=status.HTTP_404_NOT_FOUND)
    if food.user != request.user:
        raise PermissionDenied(detail={"message":"You do not have the permission to edit this item as you did not create it."})    
    
    if request.method == "GET":
        user=request.user
        if user.is_vendor == False:
            raise PermissionDenied(detail={"message":f"Permission Denied. Only vendors can perform this action"})
        serializer = FoodSerializer(food)
        
        data = {
           "message":"successful",
           "data": serializer.data
        }
    
    
        return Response(data, status=status.HTTP_200_OK)
    
    elif request.method == 'PUT':
        user=request.user
        if user.is_vendor == False:
            raise PermissionDenied(detail={"message":f"Permission Denied. Only vendors can perform this action"})
        serializer = FoodSerializer(food, data=request.data, partial=True)
        if serializer.is_valid():
                
            serializer.save()
            data = {
                'message' : 'success',
                'data'  : serializer.data
            }
            return Response(data, status=status.HTTP_202_ACCEPTED)
        else:
            data = {
                'message' : 'failed',
                'error'  : serializer.errors
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        
    elif request.method=="DELETE":
        user=request.user
        if user.is_vendor == False:
            raise PermissionDenied(detail={"message":f"Permission Denied. Only vendors can perform this action"})
        food.delete()
        
        return Response({}, status=status.HTTP_204_NO_CONTENT)
    



@swagger_auto_schema(methods=['POST'] ,
                    request_body=MenuSerializer())
@api_view(['GET', 'POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def menus(request):
    # get logged in vendors menu and manually add to menu for logged in vendor
    user= request.user
    if request.method == "GET":
        if user.is_vendor == False:
            raise PermissionDenied(detail={"message":f"Permission Denied. Only vendors can perform this action"})
        menu = Menu.objects.filter(user=user)
        serializer = MenuSerializer(menu, many=True)
        
        data = {
           "message":"successful",
           "data": serializer.data
        }
    
    
        return Response(data, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        if user.is_vendor == False:
            raise PermissionDenied(detail={"message":f"Permission Denied. Only vendors can perform this action"})
        serializer = MenuSerializer(data=request.data)
        if serializer.is_valid(): 
            if "user" in serializer.validated_data.keys():
                serializer.validated_data.pop("user")  
            food = serializer.validated_data["food"]
            check = Food.objects.filter(id=food.id,user=user)
            if check.exists():
                pass
            else:
                raise PermissionDenied(detail={"message":"You do not have the permission to add this item."})

            
            check_in_menu=Menu.objects.filter(user=user, food=food)
            if check_in_menu.exists():
                data = {
                    'message' : 'Failed. Food item already in your menu.'
                }
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
            else:
                pass
            menu = Menu.objects.create(user=user, food=food)
            new_serializer = MenuSerializer(menu)
            
            data = {
                'message' : 'success',
                'data'  : new_serializer.data
            }
            return Response(data, status=status.HTTP_202_ACCEPTED)
        else:
            data = {
                'message' : 'failed',
                'error'  : serializer.errors
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET', 'DELETE'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def menu_detail(request, menu_id):

    # get, delete an individual menu item
    try:
        food = Menu.objects.get(id=menu_id)
    except Menu.DoesNotExist:

        data = {
            'message' : 'failed',
            'error'  : f"Menu with ID {menu_id} does not exist."
        }
        return Response(data, status=status.HTTP_404_NOT_FOUND)
    if food.user != request.user:
        raise PermissionDenied(detail={"message":"You do not have the permission to view this item."})
    
    if request.method == "GET":
        user=request.user
        if user.is_vendor == False:
            raise PermissionDenied(detail={"message":f"Permission Denied. Only vendors can perform this action"})
        serializer = MenuSerializer(food)
        
        data = {
           "message":"successful",
           "data": serializer.data
        }
    
    
        return Response(data, status=status.HTTP_200_OK)
    
    elif request.method=="DELETE":
        user=request.user
        if user.is_vendor == False:
            raise PermissionDenied(detail={"message":f"Permission Denied. Only vendors can perform this action"})
        food.delete()
        
        return Response({}, status=status.HTTP_204_NO_CONTENT)
    


