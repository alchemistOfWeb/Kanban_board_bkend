import django_filters
from django_filters import rest_framework as filters
from .models import Task


class IdFilterInFilter(filters.BaseInFilter, filters.NumberFilter):
    ...


class TaskFilter(filters.FilterSet):
    # format: Y-M-d[ H[:i[:s]]]
    dl_min = filters.DateTimeFilter(field_name='deadline_at', lookup_expr='gt')
    dl_max = filters.DateTimeFilter(field_name='deadline_at', lookup_expr='lt')

    completion_min = filters.NumberFilter(field_name='completion', lookup_expr='gt')
    completion_max = filters.NumberFilter(field_name='completion', lookup_expr='lt')

    tags = IdFilterInFilter(field_name='tags__id', lookup_expr='in')

    class Meta:
        model = Task
        fields = [
            'deadline_at',
            'completion',
            'tags',
        ]
