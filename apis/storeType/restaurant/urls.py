from django.urls import path, include
from .views import  RestaurantInfoView, MenuView, MenuItemView

urlpatterns = [
    # path('', index, name='restaurant_index'),
    path('info/', RestaurantInfoView.as_view(), name='restaurant_info'),
    path('menu/', MenuView.as_view(), name='restaurant_menu_detail'),
    path('menu/item/', MenuItemView.as_view(), name='restaurant_menu_item_detail'),
]
