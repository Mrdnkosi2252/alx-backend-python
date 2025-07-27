
import django_filters
from .models import Message, Conversation

class MessageFilter(django_filters.FilterSet):
    user = django_filters.NumberFilter(field_name='conversation__participants__id')
    start_time = django_filters.DateTimeFilter(field_name='timestamp', lookup_expr='gte')
    end_time = django_filters.DateTimeFilter(field_name='timestamp', lookup_expr='lte')

    class Meta:
        model = Message
        fields = ['user', 'start_time', 'end_time']