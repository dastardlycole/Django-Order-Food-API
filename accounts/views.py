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
# Create your views here.

User = get_user_model()

# @swagger_auto_schema(method='get',
# request_body=UserSerializer()) 
@api_view(['GET'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAdminUser])
def user_view(request):

    if request.method == "GET":
        users = User.objects.all()

        serializer = UserSerializer(users,many=True)

        data = {
            "message": "success",
            "data": serializer.data
        }
        return Response(data, status = status.HTTP_200_OK)

