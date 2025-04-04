from django.urls import path,include

urlpatterns = [
    path('restaurant/', include('apis.storeType.restaurant.urls')),
]
