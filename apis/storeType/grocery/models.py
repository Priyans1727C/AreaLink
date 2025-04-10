from django.db import models
from apis.storeType.general import models as base_models
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
