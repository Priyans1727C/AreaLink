from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

class Store(models.Model):
    """
    Model to store information about a shop/store.
    Each store is owned by a registered user with the role of 'shop_owner'.
    """

    class StoreTypeChoices(models.TextChoices):
        RESTAURANTS = 'restaurants', 'Restaurants'
        GROCERY = 'grocery', 'Grocery'
        GARMENT = 'garment', 'Garment'
        ELECTRONICS = 'electronics', 'Electronics'
        FURNITURE = 'furniture', 'Furniture'
        BOOKS = 'books', 'Books'
        OTHER = 'other', 'Other'

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='stores',
        limit_choices_to={'role': 'shop_owner'},
        help_text=_("User who owns the store."),
    )
    name = models.CharField(max_length=255, unique=True, help_text=_("Store name"))
    type = models.CharField(
        max_length=20,
        choices=StoreTypeChoices.choices,
        default=StoreTypeChoices.OTHER,
        help_text=_("Type of store (e.g., Grocery, Garment, Electronics, etc.)"),
    )
    description = models.TextField(blank=True, null=True, help_text=_("Short description of the store"))
    
    # address = models.TextField(help_text=_("Full address of the store"))
    # city = models.CharField(max_length=100, help_text=_("City where the store is located"))
    # state = models.CharField(max_length=100, help_text=_("State where the store is located"))
    # pincode = models.CharField(max_length=10, help_text=_("Postal code of the store"))

    # phone = models.CharField(max_length=20, blank=True, null=True, help_text=_("Store contact number"))
    # email = models.EmailField(blank=True, null=True, help_text=_("Store email address"))

    # opening_time = models.TimeField(help_text=_("Opening time of the store"))
    # closing_time = models.TimeField(help_text=_("Closing time of the store"))

    # is_active = models.BooleanField(default=True, help_text=_("Whether the store is active or not"))

    created_at = models.DateTimeField(auto_now_add=True, help_text=_("Time when the store was created"))
    updated_at = models.DateTimeField(auto_now=True, help_text=_("Last updated timestamp"))

    def __str__(self):
        return f"{self.name} ({self.get_type_display()} - {self.owner.username})"

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Store"
        verbose_name_plural = "Stores"
