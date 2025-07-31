from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification, MessageHistory
from django.utils import timezone

class MessagingTests(TestCase):
    def setUp(self):
        self.sender = User.objects.create_user(username='sender', password='testpass123')
        self.receiver = User.objects.create_user(username='receiver', password='testpass123')
        
    def test_message_creation(self):
        message = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content="Test message"
        )
        self.assertEqual(message.sender, self.sender)
        self.assertEqual(message.receiver, self.receiver)
        self.assertEqual(message.content, "Test message")
        self.assertFalse(message.edited)
        self.assertFalse(message.read)
        self.assertTrue(message.timestamp)
        
    def test_notification_creation(self):
        message = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content="Test message"
        )
        notification = Notification.objects.get(user=self.receiver, message=message)
        self.assertEqual(notification.user, self.receiver)
        self.assertEqual(notification.message, message)
        self.assertFalse(notification.is_read)
        self.assertTrue(notification.created_at)
        
    def test_signal_triggers_notification(self):
        message = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content="Test message"
        )
        self.assertEqual(Notification.objects.count(), 1)
        notification = Notification.objects.first()
        self.assertEqual(notification.user, self.receiver)
        self.assertEqual(notification.message, message)
        
    def test_message_edit_logging(self):
        message = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content="Original message"
        )
        message.content = "Updated message"
        message.save()
        self.assertTrue(message.edited)
        self.assertEqual(MessageHistory.objects.count(), 1)
        history = MessageHistory.objects.first()
        self.assertEqual(history.message, message)
        self.assertEqual(history.old_content, "Original message")
        self.assertTrue(history.edited_at)
        
    def test_user_deletion_cascades(self):
        message = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content="Test message"
        )
        message.content = "Updated message"
        message.save()
        notification = Notification.objects.get(user=self.receiver, message=message)
        self.sender.delete()
        self.assertEqual(Message.objects.filter(sender=self.sender).count(), 0)
        self.assertEqual(Notification.objects.filter(user=self.sender).count(), 0)
        self.assertEqual(MessageHistory.objects.filter(message__sender=self.sender).count(), 0)
        
    def test_threaded_message(self):
        parent = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content="Parent message"
        )
        reply = Message.objects.create(
            sender=self.receiver,
            receiver=self.sender,
            content="Reply message",
            parent_message=parent
        )
        self.assertEqual(reply.parent_message, parent)
        self.assertIn(reply, parent.replies.all())
        
    def test_query_optimization(self):
        parent = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content="Parent message"
        )
        reply = Message.objects.create(
            sender=self.receiver,
            receiver=self.sender,
            content="Reply message",
            parent_message=parent
        )
        with self.assertNumQueries(2):
            messages = Message.objects.filter(sender=self.sender).select_related('sender', 'receiver').prefetch_related('replies')
            for message in messages:
                _ = message.sender.username
                _ = message.receiver.username
                _ = [r.content for r in message.replies.all()]
                
    def test_unread_messages_manager(self):
        Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content="Unread message",
            read=False
        )
        Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content="Read message",
            read=True
        )
        unread = Message.unread.for_user(self.receiver)
        self.assertEqual(unread.count(), 1)
        self.assertEqual(unread.first().content, "Unread message")
        
    def test_unread_messages_query_optimization(self):
        Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content="Unread message",
            read=False
        )
        with self.assertNumQueries(1):
            messages = Message.unread.for_user(self.receiver).only(
                'sender__username', 'content', 'timestamp', 'read'
            ).select_related('sender')
            for message in messages:
                _ = message.sender.username
                _ = message.content
                _ = message.timestamp
                _ = message.read