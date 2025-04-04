from .models import Store
from django.contrib import admin
# Register your models here.

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner')  # Adjust fields as per your model
    