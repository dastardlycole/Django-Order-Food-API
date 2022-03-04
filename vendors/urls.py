from django.urls import path
from . import views


urlpatterns = [
    path("vendor/food/", views.food_view),
    path("vendor/food/<int:food_id>/", views.food_detail),
    path("vendor/menus/", views.menus),
    path("vendor/menus/<int:item_id>/", views.menu_detail),
    
]