from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _
from apis.stores.models import Store
from django.conf import settings

# Create your models here.
class StoreInfo(models.Model):
    """
    Model to store information about a shop.
    Each store is owned by a registered user with the role of 'shop_owner'.
    """
    
    store = models.OneToOneField(
        Store,
        on_delete=models.CASCADE,
        related_name='store_info',
        help_text=_("User who owns the store."),
    )
    name = models.CharField(max_length=255, unique=True, help_text=_("store name"))
    description = models.TextField(blank=True, null=True, help_text=_("Short description of the store"))
    
    address = models.TextField(help_text=_("Full address of the store"))
    city = models.CharField(max_length=100, help_text=_("City where the store is located"))
    state = models.CharField(max_length=100, help_text=_("State where the store is located"))
    pincode = models.CharField(max_length=10, help_text=_("Postal code of the store"))

    phone = models.CharField(max_length=20, blank=True, null=True, help_text=_("store contact number"))
    email = models.EmailField(blank=True, null=True, help_text=_("store email address"))

    opening_time = models.TimeField(help_text=_("Opening time of the store"))
    closing_time = models.TimeField(help_text=_("Closing time of the store"))

    is_active = models.BooleanField(default=True, help_text=_("Whether the store is active or not"))

    created_at = models.DateTimeField(auto_now_add=True, help_text=_("Time when the store was created"))
    updated_at = models.DateTimeField(auto_now=True, help_text=_("Last updated timestamp"))

    class Meta:
        abstract = True




class StoreCategory(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='store_categories')
    category_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True, help_text=_("Time when the store was created"))
    updated_at = models.DateTimeField(auto_now=True, help_text=_("Last updated timestamp"))

    class Meta:
        abstract = True
         


class StoreItem(models.Model):
    menu = models.ForeignKey(StoreCategory, on_delete=models.CASCADE, related_name='store_items')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.URLField(blank=True, null=True)
    is_available = models.BooleanField(default=True)
    is_vegetarian = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, help_text=_("Time when the restaurant was created"))
    updated_at = models.DateTimeField(auto_now=True, help_text=_("Last updated timestamp"))


    class Meta:
        abstract = True
       
    
class Order(models.Model):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Processing", "Processing"),
        ("Delivered", "Delivered"),
        ("Cancelled", "Cancelled"),
    ]

    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="orders")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders")
    order_date = models.DateTimeField(auto_now_add=True)
    delivery_address = models.TextField(blank=True, null=True)
    order_status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="Pending")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    payment_method = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, help_text=_("Time when the store order was created"))
    updated_at = models.DateTimeField(auto_now=True, help_text=_("Last updated timestamp"))

    class Meta:
        abstract = True
       

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    item = models.ForeignKey(StoreItem, on_delete=models.CASCADE, related_name="order_items")
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    special_instructions = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, help_text=_("Time when the orderItem was created"))
    updated_at = models.DateTimeField(auto_now=True, help_text=_("Last updated timestamp"))

    class Meta:
        abstract = True
       
       
class CartItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="cart_items")
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="cart_items")
    item = models.ForeignKey(StoreItem, on_delete=models.CASCADE, related_name="cart_items")
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

