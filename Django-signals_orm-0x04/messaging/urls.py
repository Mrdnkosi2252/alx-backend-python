from django.urls import path
from . import views

app_name = 'messaging'
urlpatterns = [
    path('message/<int:message_id>/history/', views.message_history, name='message_history'),
    path('delete-account/', views.delete_user, name='delete_user'),
    path('conversation/<int:user_id>/', views.threaded_conversation, name='threaded_conversation'),
    path('inbox/', views.inbox, name='inbox'),
]