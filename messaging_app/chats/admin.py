from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'first_name', 'last_name', 'email', 'role', 'created_at')
    search_fields = ('email', 'first_name', 'last_name')
    list_filter = ('role', 'created_at')
