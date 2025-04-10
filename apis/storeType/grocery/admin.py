from django.contrib import admin
from .models import GroceryStoreInfo, GroceryStoreCategory, GroceryStoreItem, GroceryOrder, GroceryOrderItem

# Register your models here.
class GroceryStoreInfoAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'phone')

class GroceryStoreCategoryAdmin(admin.ModelAdmin):
    list_display = ('store', 'category_name')
    
class GroceryStoreItemAdmin(admin.ModelAdmin):
    list_display = ('category', 'item_name', 'price')
    
class  GroceryOrderAdmin(admin.ModelAdmin):
    list_display = ('store', 'user', 'created_at')
    
class GroceryOrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'item', 'quantity')


admin.site.register(GroceryOrderItem, GroceryOrderItemAdmin)
admin.site.register(GroceryOrder, GroceryOrderAdmin)
admin.site.register(GroceryStoreInfo, GroceryStoreInfoAdmin)
admin.site.register(GroceryStoreCategory, GroceryStoreCategoryAdmin)
admin.site.register(GroceryStoreItem, GroceryStoreItemAdmin)