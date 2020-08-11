from django_filters import rest_framework as filters

from api_rest.models import ErrorLog


class ErrorLogFilterSet(filters.FilterSet):
    level = filters.CharFilter(field_name="level", lookup_expr='exact')
    agent = filters.CharFilter(field_name='agent', lookup_expr='exact')
    environment = filters.CharFilter(field_name='environment', lookup_expr='exact')
    description = filters.CharFilter(field_name='description', lookup_expr='icontains')
    exception = filters.CharFilter(field_name='exception', lookup_expr='exact')
    user = filters.CharFilter(field_name='user', lookup_expr='exact')

    class Meta:
        model = ErrorLog
        fields = ['level', 'environment']
