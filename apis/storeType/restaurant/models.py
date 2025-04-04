from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from apis.stores.models import Store

# Create your models here.
class Restaurant(models.Model):
    """
    Model to store information about a shop.
    Each store is owned by a registered user with the role of 'shop_owner'.
    """
    
    store = models.OneToOneField(
        Store,
        on_delete=models.CASCADE,
        related_name='restaurant',
        help_text=_("User who owns the restaurant."),
    )
    name = models.CharField(max_length=255, unique=True, help_text=_("restaurant name"))
    description = models.TextField(blank=True, null=True, help_text=_("Short description of the restaurant"))
    
    address = models.TextField(help_text=_("Full address of the restaurant"))
    city = models.CharField(max_length=100, help_text=_("City where the restaurant is located"))
    state = models.CharField(max_length=100, help_text=_("State where the restaurant is located"))
    pincode = models.CharField(max_length=10, help_text=_("Postal code of the restaurant"))

    phone = models.CharField(max_length=20, blank=True, null=True, help_text=_("restaurant contact number"))
    email = models.EmailField(blank=True, null=True, help_text=_("restaurant email address"))

    opening_time = models.TimeField(help_text=_("Opening time of the restaurant"))
    closing_time = models.TimeField(help_text=_("Closing time of the restaurant"))

    is_active = models.BooleanField(default=True, help_text=_("Whether the restaurant is active or not"))

    created_at = models.DateTimeField(auto_now_add=True, help_text=_("Time when the restaurant was created"))
    updated_at = models.DateTimeField(auto_now=True, help_text=_("Last updated timestamp"))

    def __str__(self):
        return f"{self.name} - {self.store.name})"

    class Meta:
        ordering = ['-created_at']
        verbose_name = "restaurant"
        verbose_name_plural = "restaurants"






class Menu(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    category_name = models.CharField(max_length=100)

    def __str__(self):
        return self.category_name

class MenuItem(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.URLField(blank=True, null=True)
    is_available = models.BooleanField(default=True)
    is_vegetarian = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
    
