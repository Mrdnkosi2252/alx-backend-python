from django.contrib import admin
from .models import User, Conversation, Message

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'email', 'first_name', 'last_name', 'role', 'created_at')
    search_fields = ('email', 'first_name', 'last_name')
    list_filter = ('role', 'is_active', 'is_staff', 'is_superuser')
    ordering = ('created_at',)
    readonly_fields = ('user_id', 'created_at')

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('conversation_id', 'created_at')
    search_fields = ('conversation_id',)
    filter_horizontal = ('participants',)
    readonly_fields = ('conversation_id', 'created_at')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('message_id', 'sender', 'conversation', 'message_body', 'sent_at')
    search_fields = ('message_body', 'sender__email')
    list_filter = ('sent_at',)
    readonly_fields = ('message_id', 'sent_at')
