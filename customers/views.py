from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from vendors.models import Menu, Food
from vendors.serializers import MenuSerializer, FoodSerializer
from drf_yasg.utils import swagger_auto_schema
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError, PermissionDenied


@swagger_auto_schema(methods=['POST'] ,
                    request_body=MenuSerializer())
@api_view(['GET', 'POST'])
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