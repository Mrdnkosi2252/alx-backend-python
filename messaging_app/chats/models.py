from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
import uuid

class User(AbstractUser):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=100, null=False, blank=False)
    last_name = models.CharField(max_length=100, null=False, blank=False)
    email = models.EmailField(unique=True, null=False, blank=False)
    password_hash = models.CharField(max_length=128, null=False, blank=False)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    role = models.CharField(
        max_length=10,
        choices=[('guest', 'Guest'), ('host', 'Host'), ('admin', 'Admin')],
        default='guest',
        null=False,
        blank=False
    )
    created_at = models.DateTimeField(auto_now_add=True)

    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions_set',
        blank=True
    )

    class Meta:
        indexes = [
            models.Index(fields=['email'], name='user_email_idx'),
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"

class Conversation(models.Model):
    conversation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    participants = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['conversation_id'], name='conv_id_idx'),
        ]

    def __str__(self):
        return f"Conversation {self.conversation_id}"

class Message(models.Model):
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    message_body = models.TextField(null=False, blank=False)
    sent_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['sender'], name='msg_sender_idx'),
            models.Index(fields=['conversation'], name='msg_conv_idx'),
        ]

    def __str__(self):
        return f"Message {self.message_id} by {self.sender}"