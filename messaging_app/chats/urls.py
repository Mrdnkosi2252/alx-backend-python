from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ConversationViewSet, MessageViewSet
from messaging_app.views import home_view


router = DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')

urlpatterns = [
    path('welcome/', home_view, name='home'), 
    path('', include(router.urls)),  
]
urlpatterns = [
    path('welcome/', home_view, name='home'),
    path('', include(router.urls)),  
]
