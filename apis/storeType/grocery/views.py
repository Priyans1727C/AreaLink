from django.shortcuts import render
from rest_framework import status
from .serializers import GroceryStoreInfoSerializer, GroceryStoreCategorySerializer, GroceryStoreItemSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import GroceryStoreInfo, GroceryStoreCategory, GroceryStoreItem
from apis.stores.models import Store

# Create your views here.
class GroceryStoreInfoView(APIView):
    """
    API view for handling grocery store information.
    """
    def get(self, request, *args, **kwargs):
        """
        Get a list of all grocery stores.
        """
        store_id = request.query_params.get('store_id') or request.data.get('store_id')
        if not store_id:
            return Response({"error": "store_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            grocery_store_info = GroceryStoreInfo.objects.get(store=store_id)
            serializer = GroceryStoreInfoSerializer(grocery_store_info)
            return Response(serializer.data)
        except GroceryStoreInfo.DoesNotExist:
            return Response({"error": "Grocery store not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def post(self, request, *args, **kwargs):
        """
        Create or update grocery store information.
        """
        store_id = request.data.get('store_id')
        if not store_id:
            return Response({"error": "store_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            store_instance = Store.objects.get(id=store_id)
            grocery_store_info = GroceryStoreInfo.objects.filter(store=store_instance).first()

            if grocery_store_info:
                # Update existing
                serializer = GroceryStoreInfoSerializer(grocery_store_info, data=request.data, partial=True)
            else:
                # Create new
                serializer = GroceryStoreInfoSerializer(data={**request.data, "store": store_instance.id})

            if serializer.is_valid():
                serializer.save()
                status_code = status.HTTP_200_OK if grocery_store_info else status.HTTP_201_CREATED
                return Response(serializer.data, status=status_code)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Store.DoesNotExist:
            return Response({"error": "Store with given ID does not exist"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def delete(self, request, *args, **kwargs):
        """
        Delete grocery store information.
        """
        store_id = request.query_params.get('store_id') or request.data.get('store_id')
        if not store_id:
            return Response({"error": "store_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            grocery_store_info = GroceryStoreInfo.objects.get(store=store_id)
            grocery_store_info.delete()
            return Response({"message": "Grocery store information deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except GroceryStoreInfo.DoesNotExist:
            return Response({"error": "Grocery store not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class GroceryStoreCategoryView(APIView):
    """
    API view for handling grocery store categories.
    """
    def get(self, request, *args, **kwargs):
        """
        Get a list of all grocery store categories.
        """
        store_id = request.query_params.get('store_id') or request.data.get('store_id')
        if not store_id:
            return Response({"error": "store_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            grocery_store = Store.objects.get(id=store_id)
            categories = grocery_store.store_categories.all()
            serializer = GroceryStoreCategorySerializer(categories, many=True)
            return Response(serializer.data)
        except Store.DoesNotExist:
            return Response({"error": "Grocery store not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def post(self, request, *args, **kwargs):
        """
        Create or update grocery store categories.
        """
        store_id = request.data.get('store_id')
        category_id = request.data.get('category_id')

        if not store_id:
            return Response({"error": "store_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            store_instance = Store.objects.get(id=store_id)

            if category_id:
                try:
                    # Try to get the existing category
                    grocery_store_category = GroceryStoreCategory.objects.get(store=store_instance, id=category_id)
                    # Update existing category
                    serializer = GroceryStoreCategorySerializer(grocery_store_category, data=request.data, partial=True)
                    if serializer.is_valid():
                        serializer.save()
                        return Response(serializer.data, status=status.HTTP_200_OK)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                except GroceryStoreCategory.DoesNotExist:
                    return Response({"error": "Category with given ID does not exist for this store."}, status=status.HTTP_404_NOT_FOUND)

            else:
                # Create new category
                serializer = GroceryStoreCategorySerializer(data={**request.data, "store": store_instance.id})
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Store.DoesNotExist:
            return Response({"error": "Store with given ID does not exist"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def delete(self, request, *args, **kwargs):
        """
        Delete grocery store categories.
        """
        category_id = request.query_params.get('category_id') or request.data.get('category_id')
        store_id = request.query_params.get('store_id') or request.data.get('store_id')
        if not category_id and not store_id:
            return Response({"error": "category_id and store_id are required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            grocery_store_category = GroceryStoreCategory.objects.get(id=category_id, store=store_id)
            grocery_store_category.delete()
            return Response({"message": "Grocery store category deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except GroceryStoreCategory.DoesNotExist:
            return Response({"error": "Grocery store category not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
class GroceryStoreItemView(APIView):
    """
    API view for handling grocery store items.
    """

    def get(self, request, *args, **kwargs):
        """
        Get a list of grocery store items.
        If category_id is provided, filter items by that category.
        Else, return all items in the given store.
        """
        category_id = request.query_params.get('category_id') or request.data.get('category_id')
        store_id = request.query_params.get('store_id') or request.data.get('store_id')

        if not store_id:
            return Response({"error": "store_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            if category_id:
                # Get items from a specific category in the store
                grocery_store_category = GroceryStoreCategory.objects.get(id=category_id, store=store_id)
                items = grocery_store_category.store_items.all()
            else:
                # Get all items across all categories for the store
                items = GroceryStoreItem.objects.filter(category__store_id=store_id)

            serializer = GroceryStoreItemSerializer(items, many=True)
            return Response(serializer.data)

        except GroceryStoreCategory.DoesNotExist:
            return Response({"error": "Grocery store category not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def post(self, request, *args, **kwargs):
        """
        Create or update grocery store items.
        """
        store_id = request.data.get('store_id')
        category_id = request.data.get('category_id')
        item_id = request.data.get('item_id')

        if not store_id:
            return Response({"error": "store_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            store_instance = Store.objects.get(id=store_id)
            grocery_store_category = GroceryStoreCategory.objects.get(id=category_id, store=store_instance)

            if item_id:
                # Update existing item
                grocery_store_item = GroceryStoreItem.objects.get(id=item_id, category=grocery_store_category)
                serializer = GroceryStoreItemSerializer(grocery_store_item, data=request.data, partial=True)
            else:
                # Create new item
                serializer = GroceryStoreItemSerializer(data={**request.data, "category": grocery_store_category.id})

            if serializer.is_valid():
                serializer.save()
                status_code = status.HTTP_200_OK if item_id else status.HTTP_201_CREATED
                return Response(serializer.data, status=status_code)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Store.DoesNotExist:
            return Response({"error": "Store with given ID does not exist"}, status=status.HTTP_404_NOT_FOUND)
        except GroceryStoreCategory.DoesNotExist:
            return Response({"error": "Grocery store category not found"}, status=status.HTTP_404_NOT_FOUND)
        except GroceryStoreItem.DoesNotExist:
            return Response({"error": "Grocery store item not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def delete(self, request, *args, **kwargs):
        """
        Delete grocery store items.
        """
        item_id = request.query_params.get('item_id') or request.data.get('item_id')
        store_id = request.query_params.get('store_id') or request.data.get('store_id')
        if not item_id and not store_id:
            return Response({"error": "item_id and store_id are required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            grocery_store_item = GroceryStoreItem.objects.get(id=item_id, category__store=store_id)
            grocery_store_item.delete()
            return Response({"message": "Grocery store item deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except GroceryStoreItem.DoesNotExist:
            return Response({"error": "Grocery store item not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)