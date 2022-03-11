from django.urls import path
from . import views


urlpatterns = [
    path("customer/menus/<int:user_id>/", views.customer_menus),
    path("customer/carts/get", views.get_carts),
    path("customer/carts/delete/<int:item_id>", views.delete_carts),
    path("customer/carts/make/<int:user_id>/", views.make_carts),
    path("customer/order/", views.create_order),
    path("customer/order/get/", views.get_orders),
    path("customer/order/delete/", views.delete_orders),
    
]