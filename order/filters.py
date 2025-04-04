from django_filters import rest_framework as filters
from .models import Order
from django.db.models import Q

class OrderFilter(filters.FilterSet):
    status = filters.CharFilter(field_name='status')
    payment_status = filters.CharFilter(field_name='payment_status')
    date_from = filters.DateFilter(field_name='created_at', lookup_expr='gte')
    date_to = filters.DateFilter(field_name='created_at', lookup_expr='lte')
    search = filters.CharFilter(method='filter_search')

    class Meta:
        model = Order
        fields = ['status', 'payment_status', 'date_from', 'date_to', 'search']

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(id__icontains=value) |
            Q(user__email__icontains=value) |
            Q(user__first_name__icontains=value) |
            Q(user__last_name__icontains=value) |
            Q(phone_no__icontains=value)
        )