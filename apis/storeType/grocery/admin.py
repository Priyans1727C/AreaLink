from django.contrib import admin
from .models import GroceryStoreInfo, GroceryStoreCategory, GroceryStoreItem

# Register your models here.
class GroceryStoreInfoAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'phone')

class GroceryStoreCategoryAdmin(admin.ModelAdmin):
    list_display = ('store', 'category_name')
    
class GroceryStoreItemAdmin(admin.ModelAdmin):
    list_display = ('category', 'item_name', 'price')
    
admin.site.register(GroceryStoreInfo, GroceryStoreInfoAdmin)
admin.site.register(GroceryStoreCategory, GroceryStoreCategoryAdmin)
admin.site.register(GroceryStoreItem, GroceryStoreItemAdmin)