from django.urls import path
from . import views


urlpatterns = [
    path("customer/menus/<int:user_id>/", views.customer_menus),
    
]