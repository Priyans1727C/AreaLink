from rest_framework import serializers
from .models import Restaurant

class RestaurantInfoSerializer(serializers.ModelSerializer):
    """
    Serializer for the Restaurant model.
    """
    class Meta:
        model = Restaurant
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
        