from django.urls import path, include
from .views import  GroceryStoreInfoView, GroceryStoreCategoryView, GroceryStoreItemView

urlpatterns = [
    path('info/', GroceryStoreInfoView.as_view(), name='grocery_store_info'),
    path('category/', GroceryStoreCategoryView.as_view(), name='grocery_store_category'),
    path('items/', GroceryStoreItemView.as_view(), name='grocery_store_item'),
    
]