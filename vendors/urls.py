from django.urls import path
from . import views


urlpatterns = [
    path("vendor/food/create", views.food_view),
    path("vendor/food/<int:food_id>/", views.food_detail),
    path("vendor/menus/", views.menus),
    path("vendor/menus/<int:menu_id>/", views.menu_detail),
    
]