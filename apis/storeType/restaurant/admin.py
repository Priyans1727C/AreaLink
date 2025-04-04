from django.contrib import admin
from .models import Restaurant
# Register your models here.

class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'store', 'is_active', 'created_at')
    search_fields = ('name', 'owner__username')
    list_filter = ('is_active', 'created_at')
    ordering = ('-created_at',)
    list_per_page = 20

admin.site.register(Restaurant, RestaurantAdmin)

