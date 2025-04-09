from django.db import models
from apis.storeType.general import models as base_models
# Create your models here.

class GroceryStoreInfo(base_models.StoreInfo):
    """
    Model to store information about a grocery store.
    Each grocery store is owned by a registered user with the role of 'shop_owner'.
    """
    pass