from django.urls import path
from . import views


urlpatterns = [
    path('admins/users/get', views.user_view, name="users"),
    path("admins/customer/order/get/", views.get_orders),
    path("admins/customer/order/delete/", views.delete_all_orders),
    path("admins/vendor/food/delete/", views.delete_all_food),
    path("admins/customer/cart/delete/", views.delete_all_carts),
    path("admins/vendor/order/delete/", views.delete_all_menus),
    path("admins/vendor/food/get", views.get_food),

]