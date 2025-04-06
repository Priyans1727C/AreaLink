from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Restaurant, Menu, MenuItem
from .serializers import RestaurantInfoSerializer, MenuSerializer, MenuItemSerializer, OrderSerializer, OrderItemSerializer
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

class RestaurantInfoView(generics.GenericAPIView):
    serializer_class = RestaurantInfoSerializer
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='store_id',         # The name of the query parameter
                description='Optional ID of the store to filter data for.', # Description for docs
                required=False,         # Set to True if the parameter is mandatory
                type=OpenApiTypes.INT,  # Use INT, STR, UUID, BOOL, DATE, DATETIME etc.
                                        # Or use simple Python types: int, str, bool
                location=OpenApiParameter.QUERY # Specify this is a query parameter
                                                # Other options: PATH, HEADER, COOKIE
            ),
            # Add more OpenApiParameter instances here if you have other query params
        ],
        # You can add other extend_schema arguments like responses, summary etc.
        summary="Retrieve data, optionally filtered by store ID",
        responses={200: OpenApiTypes.OBJECT} # Example response
    )
    def get(self, request, *args, **kwargs):
        """
        Retrieve restaurant information.
        If store_id is provided, it will return the restaurant information for that store.
        """
        
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
        """
        Add a new restaurant entry.
        The request should contain a JSON object with the restaurant details.
        """
        
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
        """
        Update an existing restaurant entry.
        The request should contain a JSON object with the updated restaurant details.
        """
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
        """
        Delete an existing restaurant entry.
        The request should contain the store_id of the restaurant to be deleted.
        """
        store_id = request.query_params.get('store_id')
        if not store_id:
            return Response({"error": "store_id is required", "params": "/?store_id=<int>"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            restaurant = Restaurant.objects.get(store_id=store_id)
            restaurant.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Restaurant.DoesNotExist:
            return Response({"error": "Restaurant not found for the given store_id"}, status=status.HTTP_404_NOT_FOUND)
        

class MenuView(APIView):
    """
    Handles CRUD operations for Restaurant Menus.
    """

    def get_restaurant(self, store_id):
        try:
            return Restaurant.objects.get(store_id=store_id)
        except Restaurant.DoesNotExist:
            return None

    def get(self, request, *args, **kwargs):
        store_id = request.query_params.get('store_id')
        if not store_id:
            return Response({"error": "store_id is required", "params": "/?store_id=<int>"}, status=status.HTTP_400_BAD_REQUEST)

        restaurant = self.get_restaurant(store_id)
        if not restaurant:
            return Response({"error": "Restaurant not found for the given store_id"}, status=status.HTTP_404_NOT_FOUND)

        menus = restaurant.menus.all()
        serializer = MenuSerializer(menus, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        store_id = request.data.get('store_id')
        if not store_id:
            return Response({"error": "store_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        restaurant = self.get_restaurant(store_id)
        if not restaurant:
            return Response({"error": "Restaurant not found for the given store_id"}, status=status.HTTP_404_NOT_FOUND)

        serializer = MenuSerializer(data=request.data.get('attributes', request.data))
        if serializer.is_valid():
            serializer.save(restaurant=restaurant)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        store_id = request.data.get('store_id')
        menu_id = request.data.get('menu_id')

        if not store_id or not menu_id:
            return Response({"error": "store_id and menu_id are required"}, status=status.HTTP_400_BAD_REQUEST)

        restaurant = self.get_restaurant(store_id)
        if not restaurant:
            return Response({"error": "Restaurant not found for the given store_id"}, status=status.HTTP_404_NOT_FOUND)

        try:
            menu = restaurant.menus.get(id=menu_id)
        except Menu.DoesNotExist:
            return Response({"error": "Menu not found with the given id"}, status=status.HTTP_404_NOT_FOUND)

        serializer = MenuSerializer(menu, data=request.data.get('attributes', request.data), partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        store_id = request.query_params.get('store_id') or request.data.get('store_id')
        menu_id = request.query_params.get('menu_id') or request.data.get('menu_id')

        if not store_id or not menu_id:
            return Response({"error": "store_id and menu_id are required"}, status=status.HTTP_400_BAD_REQUEST)

        restaurant = self.get_restaurant(store_id)
        if not restaurant:
            return Response({"error": "Restaurant not found for the given store_id"}, status=status.HTTP_404_NOT_FOUND)

        try:
            menu = restaurant.menus.get(id=menu_id)
        except Menu.DoesNotExist:
            return Response({"error": "Menu not found with the given id"}, status=status.HTTP_404_NOT_FOUND)

        menu.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
    
class MenuItemView(APIView):
    """
    Handles CRUD operations for Menu Items.
    """

    def get_menu(self, store_id, menu_id):
        try:
            restaurant = Restaurant.objects.get(store_id=store_id)
            return restaurant.menus.get(id=menu_id)
        except (Restaurant.DoesNotExist, Menu.DoesNotExist):
            return None
    def get(self, request, *args, **kwargs):
        store_id = request.query_params.get('store_id') or request.data.get('store_id')
        menu_id = request.query_params.get('menu_id') or request.data.get('menu_id')

        if not store_id or not menu_id:
            return Response({"error": "store_id and menu_id are required", "params": "/?store_id=<int>&menu_id=<int>"}, status=status.HTTP_400_BAD_REQUEST)

        menu = self.get_menu(store_id, menu_id)
        if not menu:
            return Response({"error": "Menu not found for the given store_id and menu_id"}, status=status.HTTP_404_NOT_FOUND)

        menu_items = menu.menu_items.all()
        serializer = MenuItemSerializer(menu_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def post(self, request, *args, **kwargs):
        store_id = request.data.get('store_id')
        menu_id = request.data.get('menu_id')
        request.data['menu'] = menu_id

        if not store_id or not menu_id:
            return Response({"error": "store_id and menu_id are required"}, status=status.HTTP_400_BAD_REQUEST)

        menu = self.get_menu(store_id, menu_id)
        if not menu:
            return Response({"error": "Menu not found for the given store_id and menu_id"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = MenuItemSerializer(data=request.data.get('attributes', request.data))
        if serializer.is_valid():
            serializer.save(menu=menu)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def put(self, request, *args, **kwargs):
        store_id = request.data.get('store_id')
        menu_id = request.data.get('menu_id')
        item_id = request.data.get('item_id')
        request.data['menu'] = menu_id

        if not store_id or not menu_id or not item_id:
            return Response({"error": "store_id, menu_id and item_id are required"}, status=status.HTTP_400_BAD_REQUEST)

        menu = self.get_menu(store_id, menu_id)
        if not menu:
            return Response({"error": "Menu not found for the given store_id and menu_id"}, status=status.HTTP_404_NOT_FOUND)

        try:
            item = menu.menu_items.get(id=item_id)
        except MenuItem.DoesNotExist:
            return Response({"error": "MenuItem not found with the given id"}, status=status.HTTP_404_NOT_FOUND)

        serializer = MenuItemSerializer(item, data=request.data.get('attributes', request.data), partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, *args, **kwargs):
        store_id = request.query_params.get('store_id') or request.data.get('store_id')
        menu_id = request.query_params.get('menu_id') or request.data.get('menu_id')
        item_id = request.query_params.get('item_id') or request.data.get('item_id')

        if not store_id or not menu_id or not item_id:
            return Response({"error": "store_id, menu_id and item_id are required"}, status=status.HTTP_400_BAD_REQUEST)

        menu = self.get_menu(store_id, menu_id)
        if not menu:
            return Response({"error": "Menu not found for the given store_id and menu_id"}, status=status.HTTP_404_NOT_FOUND)

        try:
            item = menu.menu_items.get(id=item_id)
        except MenuItem.DoesNotExist:
            return Response({"error": "MenuItem not found with the given id"}, status=status.HTTP_404_NOT_FOUND)

        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    