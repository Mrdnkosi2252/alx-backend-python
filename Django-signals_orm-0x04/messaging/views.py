from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.cache import cache_page
from .models import Message

@login_required
def message_history(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    history = message.history.all()
    return render(request, 'messaging/message_history.html', {'message': message, 'history': history})

@login_required
def delete_user(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        return HttpResponseRedirect(reverse('login'))
    return render(request, 'messaging/delete_user.html')

@login_required
@cache_page(60)
def threaded_conversation(request, user_id):
    other_user = get_object_or_404(User, id=user_id)
    messages = Message.objects.filter(
        sender=request.user, receiver=other_user
    ).select_related('sender', 'receiver').prefetch_related('replies') | Message.objects.filter(
        sender=other_user, receiver=request.user
    ).select_related('sender', 'receiver').prefetch_related('replies')
    
    def get_all_replies(message, all_messages=None):
        if all_messages is None:
            all_messages = []
        all_messages.append(message)
        for reply in message.replies.all():
            get_all_replies(reply, all_messages)
        return all_messages
    
    threaded_messages = []
    for message in messages:
        if not message.parent_message:
            threaded_messages.extend(get_all_replies(message))
    
    return render(request, 'messaging/threaded_conversation.html', {
        'other_user': other_user,
        'messages': threaded_messages
    })

@login_required
def inbox(request):
    unread_messages = Message.unread.unread_for_user(request.user).only(
        'sender__username', 'content', 'timestamp', 'read'
    ).select_related('sender')
    return render(request, 'messaging/inbox.html', {'unread_messages': unread_messages})
