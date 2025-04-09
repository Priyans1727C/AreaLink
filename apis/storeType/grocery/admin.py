from django.contrib import admin
from .models import GroceryStoreInfo

# Register your models here.
class GroceryStoreInfoAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'phone')


admin.site.register(GroceryStoreInfo, GroceryStoreInfoAdmin)