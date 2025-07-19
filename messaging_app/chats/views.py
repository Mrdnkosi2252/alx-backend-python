from rest_framework import generics
from .models import Conversation
from .serializers import ConversationSerializer

class ConversationListCreate(generics.ListCreateAPIView):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
