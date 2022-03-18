from django.urls import path
from . import views


urlpatterns = [
    path("customer/menus/<int:vendor_user_id>/", views.customer_menus),
    path("customer/carts/get", views.get_carts),
    path("customer/carts/delete/<int:item_id>", views.delete_carts),
    path("customer/carts/add/<int:vendor_user_id>/", views.make_carts),
    path("customer/find_vendors_by_location/<str:location>/", views.vendors_by_location),
    path("customer/order/", views.create_order),
    
]