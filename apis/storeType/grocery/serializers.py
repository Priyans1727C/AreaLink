from rest_framework import serializers
from .models import GroceryStoreInfo, GroceryStoreCategory

class GroceryStoreInfoSerializer(serializers.ModelSerializer):
    """
    Serializer for the GroceryStoreInfo model.
    """
    class Meta:
        model = GroceryStoreInfo
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']
        extra_kwargs = {
            'name': {'required': True},
            'description': {'required': False},
            'address': {'required': True},
            'city': {'required': True},
            'state': {'required': True},
            'pincode': {'required': True},
            'phone': {'required': False},
            'email': {'required': False},
            'opening_time': {'required': True},
            'closing_time': {'required': True},
            'is_active': {'required': False}
        }
        
class GroceryStoreCategorySerializer(serializers.ModelSerializer):
    """
    Serializer for the GroceryStoreCategory model.
    """
    class Meta:
        model = GroceryStoreCategory
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']
        extra_kwargs = {
            'store': {'required': True},
            'name': {'required': True},
            'type': {'required': True},
            'description': {'required': False}
        }