from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from vendors.models import Menu, Food
from .models import Cart, Order
from django.contrib.auth import get_user_model
from vendors.serializers import MenuSerializer, FoodSerializer
from .serializers import CartSerializer, OrderSerializer
from drf_yasg.utils import swagger_auto_schema
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError, PermissionDenied
User = get_user_model()

@api_view(['GET'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def customer_menus(request,user_id):
    # user= request.user
    if request.method == "GET":
        menu = Menu.objects.filter(user=user_id)
        if menu.exists():
            pass
        else:
            data = {
            'message' : 'failed',
            'error'  : f"Menu does not exist."
        }
            return Response(data, status=status.HTTP_404_NOT_FOUND)
        serializer = MenuSerializer(menu, many=True)
        
        data = {
           "message":"successful",
           "data": serializer.data
        }
    
    
        return Response(data, status=status.HTTP_200_OK)



@api_view(['GET'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def get_carts(request):
    user= request.user
    if request.method == "GET":
        cart = Cart.objects.filter(user=user)
        serializer = CartSerializer(cart, many=True)
        
        data = {
           "message":"successful",
           "data": serializer.data
        }
    
    
        return Response(data, status=status.HTTP_200_OK)

@swagger_auto_schema(methods=['POST'] ,
                    request_body=MenuSerializer())
@api_view(['POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def make_carts(request,user_id): 
    user=request.user  #user creating cart 
    if request.method == 'POST':
        serializer = CartSerializer(data=request.data)
        if serializer.is_valid(): 
            if "user" in serializer.validated_data.keys():
                serializer.validated_data.pop("user")  
            food = serializer.validated_data["food"]
            ven=User.objects.filter(id=user_id)
            if ven.exists():
                pass
            else:
                data = {
                'message' : 'Vendor does not exist',
            }
                return Response(data, status=status.HTTP_400_BAD_REQUEST)

            check = Menu.objects.filter(food=food,user=User.objects.get(id=user_id))
            if check.exists():
                pass
            else:
                raise PermissionDenied(detail={"message":f"Vendor {user_id} does not have this item this item."}) 

            
            if len(Cart.objects.filter(user=user)) != 0:
                diff_vens=Cart.objects.filter(user=user).first() #checks if the item has a diff vendor from what is already in cart
                if diff_vens.food.user.id != user_id:
                    data = {
                    'message' : 'Cart can only contain food from one vendor',
                }
                    return Response(data, status=status.HTTP_400_BAD_REQUEST)


            

            cart = Cart.objects.create(user=user, food=food)
            new_serializer = CartSerializer(cart)
            
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


@api_view(['DELETE'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def delete_carts(request,item_id): 
    user=request.user  #user creating cart 
    if request.method == 'DELETE':
        try:
            cart = Cart.objects.get(user=user,id=item_id)
        except Cart.DoesNotExist:

            data = {
                'message' : 'failed',
                'error'  : f"Cart does not exist."
            }
            return Response(data, status=status.HTTP_404_NOT_FOUND)

        cart.delete()
        return Response({}, status=status.HTTP_204_NO_CONTENT)    
       

       

@swagger_auto_schema(methods=['POST'] ,
                    request_body=OrderSerializer())
@api_view(['POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def create_order(request):
    user=request.user
    if request.method == "POST":
    
        cart = Cart.objects.filter(user=user)
        first_serializer = CartSerializer(cart, many=True)
        
        if len(first_serializer.data) == 0:

            data = {
                'message' : 'failed',
                'error'  : f"Your cart is empty."
            }

            return Response(data, status=status.HTTP_404_NOT_FOUND)
    

        total=0
        for i in first_serializer.data:
            total+=i['cart_food_detail']['price']

         #Allows user to signup or create account
        serializer = OrderSerializer(data=request.data) #deserialize the data
        if serializer.is_valid(): #validate the data that was passed            
            #  fixed by removing serializer.save
            address=serializer.validated_data["address"]        
            message=serializer.validated_data["message"]        
            payment_choice=serializer.validated_data["payment_choice"]        
            order = Order.objects.create(user=user,address=address,message=message,payment_choice=payment_choice)
            new_order_serializer = OrderSerializer(order)
            
            
            
            data = {
                'message' : 'success',
                'data'  : new_order_serializer.data,
                'cart items': first_serializer.data,
                'Total Bill' : total
                
            }
            for i in cart:
                i.delete()
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            data = {
                'message' : 'failed',
                'error'  : serializer.errors
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
    
# get all orders and delete all orders not necessary only for super user
#actually nah we need order history for vendor and customer
@api_view(['GET'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def get_orders(request):
    user= request.user
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
def delete_orders(request,): 
    user=request.user  #user creating cart 
    if request.method == 'DELETE':
        order = Order.objects.all()
        for i in order:
            i.delete()

        return Response({}, status=status.HTTP_204_NO_CONTENT)    




       

                