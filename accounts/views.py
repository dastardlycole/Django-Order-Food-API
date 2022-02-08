from functools import partial
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import status 
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from .serializers import UserSerializer
from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.auth import authenticate
from django.forms import model_to_dict
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.exceptions import ValidationError

from accounts import serializers
# Create your views here.

User = get_user_model()


@api_view(['GET'])
# @authentication_classes([BasicAuthentication])
# @permission_classes([IsAdminUser])
def user_view(request):

    users = User.objects.all()

    serializer = UserSerializer(users,many=True)

    data = {
        "message": "success",
        "data": serializer.data
    }
    return Response(data, status = status.HTTP_200_OK)

@swagger_auto_schema(method='post',
request_body=UserSerializer())
@api_view(['POST'])
def create_user_view(request):
    serializer = UserSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save()

        data = {
            "message" : "success",
            "data" : serializer.data
        }
        return Response(data, status=status.HTTP_201_CREATED)
    else:
        data = {
            "message" : "failure",
            "error" : serializer.errors
        }
        return Response(data, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(method='put',
request_body=UserSerializer())
@api_view(['GET','PUT','DELETE'])
@authentication_classes([BasicAuthentication]) 
@permission_classes([IsAuthenticated])
def edit_user_view(request):
    user = request.user

    if request.method == 'GET':
        serializer = UserSerializer(user)

        data = {
            "message": "successful",
            "data": serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)

    elif request.method == "PUT":
        serializer=UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            if 'password' in serializer.validated_data.keys():
                raise ValidationError(detail = {"message": "Edit password action not allowed"}, code=status.HTTP_403_FORBIDDEN)

            serializer.save()

            data= {
                "message": "successful",
                "data": serializer.data,
            }
            return Response(data, status=status.HTTP_202_ACCEPTED)
        else:

            data = {
                "message" : "failure",
                "error" : serializer.errors
            }    
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        user.delete()       

        return Response({}, status=status.HTTP_204_NO_CONTENT)

