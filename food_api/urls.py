"""food_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title = "Order Food API",
        default_version = "v1",
        description = """
        This is an API for ordering food online based on location.
        Created by Ifemide Cole
        github : https://github.com/dastardlycole/Django-Order-Food-API
        linkedin : https://www.linkedin.com/in/ifemide-cole/


        For admin privileges contact the developer
        """,
        terms_of_service = "",
        contact = openapi.Contact(email="ifemidecole@gmail.com"),
        license  = openapi.License(name="MIT License"),
    ),
    public = True,
    permission_classes = [permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('v1/account/',include('accounts.urls')),
    path('v1/', include('vendors.urls')),
    path('v1/', include('customers.urls')),
    path('v1/', include('admins.urls')),
    path("", schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
