from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Create a new conversation and associate it with the authenticated user
        conversation = serializer.save()
        conversation.participants.add(self.request.user)
        conversation.save()

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filter messages by conversations the authenticated user is part of
        user = self.request.user
        return Message.objects.filter(conversation__participants=user)

    def perform_create(self, serializer):
        # Ensure the authenticated user is a participant in the conversation
        conversation_id = self.request.data.get('conversation')
        conversation = Conversation.objects.get(id=conversation_id)
        if self.request.user not in conversation.participants.all():
            raise PermissionError("You are not a participant in this conversation.")
        serializer.save(sender=self.request.user, conversation=conversation)