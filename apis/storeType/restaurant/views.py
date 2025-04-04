from rest_framework import generics, status
from rest_framework.response import Response
from .models import Restaurant
from .serializers import RestaurantInfoSerializer

class RestaurantInfoView(generics.GenericAPIView):
    serializer_class = RestaurantInfoSerializer

    def get(self, request, *args, **kwargs):
        store_id = request.query_params.get('store_id')
        if not store_id:
            return Response({"error": "store_id is required", "params": "/?store_id=<int>"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            restaurant = Restaurant.objects.get(store_id=store_id)
            serializer = self.get_serializer(restaurant)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Restaurant.DoesNotExist:
            return Response({"error": "Restaurant not found for the given store_id"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, *args, **kwargs):
        store_id = request.data.get('store')
        print(type(request.data))
        if not store_id:
            return Response({"error": "store_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        if Restaurant.objects.filter(store_id=store_id).exists():
            return Response({"error": "A Restaurant already exists for the given store_id"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data.get('attributes', request.data)) # Handles both nested and non-nested data.
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        store_id = request.data.get('store')
        if not store_id:
            return Response({"error": "store_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            restaurant = Restaurant.objects.get(store_id=store_id)
            serializer = self.get_serializer(restaurant, data=request.data.get('attributes', request.data), partial=True) #handles nested and non-nested data.
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Restaurant.DoesNotExist:
            return Response({"error": "Restaurant not found for the given store_id"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, *args, **kwargs):
        store_id = request.query_params.get('store_id')
        if not store_id:
            return Response({"error": "store_id is required", "params": "/?store_id=<int>"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            restaurant = Restaurant.objects.get(store_id=store_id)
            restaurant.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Restaurant.DoesNotExist:
            return Response({"error": "Restaurant not found for the given store_id"}, status=status.HTTP_404_NOT_FOUND)