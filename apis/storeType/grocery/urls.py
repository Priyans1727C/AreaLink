from django.urls import path, include
from .views import  GroceryStoreInfoView

urlpatterns = [
    path('info/', GroceryStoreInfoView.as_view(), name='grocery_store_info'),
]