from django.contrib import admin
from .models import GroceryStoreInfo, GroceryStoreCategory

# Register your models here.
class GroceryStoreInfoAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'phone')

class GroceryStoreCategoryAdmin(admin.ModelAdmin):
    list_display = ('store', 'category_name')
    
admin.site.register(GroceryStoreInfo, GroceryStoreInfoAdmin)
admin.site.register(GroceryStoreCategory, GroceryStoreCategoryAdmin)