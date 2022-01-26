import django_filters
from django_filters import rest_framework as filters
from .models import Task


class IdFilterInFilter(filters.BaseInFilter, filters.NumberFilter):
    ...


class TaskFilter(filters.FilterSet):
    # deadline_at = filters.DateTimeFromToRangeFilter()
    # deadline_at_after: 2022-03-02 18:00, deadline_at_before: 2022-01-01 8:00
    # completion = filters.RangeFilter()
    # completion_min: 90, completion_max: 100

    deadline__gt = filters.NumberFilter(field_name='deadline_at', lookup_expr='gt')
    deadline__lt = filters.NumberFilter(field_name='deadline_at', lookup_expr='lt')

    completion__gt = filters.NumberFilter(field_name='completion', lookup_expr='gt')
    completion__lt = filters.NumberFilter(field_name='completion', lookup_expr='lt')

    tags = IdFilterInFilter(field_name='tags__id', lookup_expr='in')

    class Meta:
        model = Task
        fields = [
            'deadline_at',
            'completion',
            'tags',
        ]
