from django_filters import rest_framework as filters
from .models import Task


class TaskFilter(filters.FilterSet):
    deadline_at = filters.DateTimeFromToRangeFilter()
    # deadline_at_after: 2022-03-02 18:00, deadline_at_before: 2022-01-01 8:00
    completion = filters.RangeFilter() 
    # completion_min: 90, completion_max: 100

    class Meta:
        model = Task
        fields = ['deadline_at', 'completion', 'tags']
