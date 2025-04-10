from django.urls import path, include
from .views import  GroceryStoreInfoView, GroceryStoreCategoryView

urlpatterns = [
    path('info/', GroceryStoreInfoView.as_view(), name='grocery_store_info'),
    path('category/', GroceryStoreCategoryView.as_view(), name='grocery_store_category'),
    
]