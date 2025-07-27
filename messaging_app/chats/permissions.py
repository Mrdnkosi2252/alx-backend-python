
from rest_framework import permissions
from .models import Conversation, Message  

class IsParticipantOfConversation(permissions.BasePermission):
    def has_permission(self, request, view):
        # Allow authenticated users
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """ Allow participants to manage their conversations/messages """
        if isinstance(obj, Conversation):
            return obj.participants.filter(id=request.user.id).exists()
        elif isinstance(obj, Message):
            return obj.conversation.participants.filter(id=request.user.id).exists()
        return False