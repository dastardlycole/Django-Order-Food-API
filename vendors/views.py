from turtle import title
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
@api_view(['GET', 'POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def food_view(request):
    user = request.user
    # get all food in the database
    if request.method == "GET":
        food_items = Food.objects.all()
        serializer = FoodSerializer(food_items, many=True)
        
        data = {
           "message":"successful",
           "data": serializer.data
        }
    
    
        return Response(data, status=status.HTTP_200_OK)
    # add food to database and menu
    elif request.method == 'POST':
        serializer = FoodSerializer(data=request.data)
        if serializer.is_valid(): 
            if "user" in serializer.validated_data.keys():
                serializer.validated_data.pop("user") 
            title = serializer.validated_data['title']    
            description = serializer.validated_data['description']    
            category = serializer.validated_data['category']    
            price = serializer.validated_data['price']       
            food = Food.objects.create(title=title,description=description,category=category,price=price,user=user)           
            new_serializer=FoodSerializer(food) 
            check = Food.objects.filter(title=title,description=description,category=category,price=price,user=user)           
            if check.exists():
                raise PermissionDenied(detail={"message":"You already have this item"})
            Menu.objects.create(food=food,user=user)
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
        
    
    
    

    
    
@swagger_auto_schema(methods=['put'] ,
                    request_body=FoodSerializer())
@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def food_detail(request, food_id):

    
    try:
        food = Food.objects.get(id=food_id)
    except Food.DoesNotExist:

        data = {
            'message' : 'failed',
            'error'  : f"Food item with ID {food_id} does not exist."
        }
        return Response(data, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == "GET":
        serializer = FoodSerializer(food)
        
        data = {
           "message":"successful",
           "data": serializer.data
        }
    
    
        return Response(data, status=status.HTTP_200_OK)
    
    elif request.method == 'PUT':
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
        food.delete()
        
        return Response({}, status=status.HTTP_204_NO_CONTENT)
    



@swagger_auto_schema(methods=['POST'] ,
                    request_body=MenuSerializer())
@api_view(['GET', 'POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def menus(request):
    user= request.user
    if request.method == "GET":
        menu = Menu.objects.filter(user=user)
        serializer = MenuSerializer(menu, many=True)
        
        data = {
           "message":"successful",
           "data": serializer.data
        }
    
    
        return Response(data, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
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
def menu_detail(request, item_id):

    
    try:
        food = Menu.objects.get(id=item_id)
    except Menu.DoesNotExist:

        data = {
            'message' : 'failed',
            'error'  : f"Menu with ID {item_id} does not exist."
        }
        return Response(data, status=status.HTTP_404_NOT_FOUND)
    if food.user != request.user:
        raise PermissionDenied(detail={"message":"You do not have the permission to view this item."})
    
    if request.method == "GET":
        serializer = MenuSerializer(food)
        
        data = {
           "message":"successful",
           "data": serializer.data
        }
    
    
        return Response(data, status=status.HTTP_200_OK)
    
    elif request.method=="DELETE":
        food.delete()
        
        return Response({}, status=status.HTTP_204_NO_CONTENT)
    


