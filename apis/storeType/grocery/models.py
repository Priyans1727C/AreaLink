from django.db import models
from apis.storeType.general import models as base_models
from apis.stores.models import Store
from django.conf import settings
# Create your models here.

class GroceryStoreInfo(base_models.StoreInfo):
    """
    Model to store information about a grocery store.
    Each grocery store is owned by a registered user with the role of 'shop_owner'.
    """
    pass


class GroceryStoreCategory(base_models.StoreCategory):
    """
    Model to store categories of grocery items.
    Each category is related to a specific grocery store.
    """
    pass


class GroceryStoreItem(base_models.StoreItem):
    """
    Model to store items in a grocery store.
    Each item is related to a specific category in the grocery store.
    """
    category = models.ForeignKey(GroceryStoreCategory, on_delete=models.CASCADE, related_name='store_items')


class GroceryOrder(base_models.Order):
    """
    Model to create order in grocery store.
    Each order is related to a specific grocery store and contains items from that store.
    """
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="grocery_orders")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="grocery_orders")
    

class GroceryOrderItem(base_models.OrderItem):
    """
    Model to store items in a grocery order.
    Each order item is related to a specific grocery order and contains details about the item.
    """
    order = models.ForeignKey(GroceryOrder, on_delete=models.CASCADE, related_name="grocery_order_items")
    item = models.ForeignKey(GroceryStoreItem, on_delete=models.CASCADE, related_name="grocery_order_items")
    
    
class GroceryCartItem(base_models.CartItem):
    """
    Model to create cart in grocery store.
    Each cart is related to a specific grocery store and contains items from that store.
    """
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="grocery_cart")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="grocery_cart")
    item = models.ForeignKey(GroceryStoreItem, on_delete=models.CASCADE, related_name="grocery_cart_items")
