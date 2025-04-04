from django.contrib import admin
from .models import User, UserProfile
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'is_staff', 'is_active')
    search_fields = ('username', 'email')
    list_filter = ('is_staff', 'is_active')
    ordering = ('-date_joined',)
    list_per_page = 20

admin.site.register(User, UserAdmin)

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'phone')
    search_fields = ('user__username', 'first_name', 'last_name')
    list_filter = ('user__is_staff',)
    ordering = ('user__date_joined',)
    list_per_page = 20
    
admin.site.register(UserProfile, UserProfileAdmin)

