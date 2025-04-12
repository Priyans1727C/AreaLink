from django.urls import path, include
from .views import  GroceryStoreInfoView, GroceryStoreCategoryView, GroceryStoreItemView, GroceryOrderView, GroceryOrderItemView, GroceryCartItemView

urlpatterns = [
    
    #curd views
    path('info/', GroceryStoreInfoView.as_view(), name='grocery_store_info'),
    path('category/', GroceryStoreCategoryView.as_view(), name='grocery_store_category'),
    path('category/items/', GroceryStoreItemView.as_view(), name='grocery_store_item'),
    path('order/', GroceryOrderView.as_view(), name='grocery_order'),
    path('order/items/', GroceryOrderItemView.as_view(), name='grocery_order_item'),
    path('cart/', GroceryCartItemView.as_view(), name='grocery_cart_item'),
    
    #frontend views
    
]