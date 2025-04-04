from django.urls import path, include
from .views import  RestaurantInfoView

urlpatterns = [
    # path('', index, name='restaurant_index'),
    path('info/', RestaurantInfoView.as_view(), name='restaurant_detail'),
]
