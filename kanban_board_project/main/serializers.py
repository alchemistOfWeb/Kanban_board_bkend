from rest_framework import serializers
from .models import Board, Task, TodoList, TaskTag
import datetime


class BoardSerializer(serializers.ModelSerializer):
    tasks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    todolists = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Board
        fields = '__all__'


class TaskTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskTag
        fields = '__all__'


class FilteredTaskSerializer(serializers.ListSerializer):
    allow_orderby_params = ['completion',
                            '-completion', 'deadline_at', '-deadline_at']
    tags = TaskTagSerializer(many=True)

    def deadline_range_filter(self, data, q_params, date_format='%Y-%m-%d %H:%M'):
        dl_min = q_params.get('dl_min')
        dl_max = q_params.get('dl_max')

        if dl_min:
            dl_min = datetime.datetime.strptime(
                q_params['dl_min'], date_format)

        if dl_max:
            dl_max = datetime.datetime.strptime(
                q_params['dl_max'], date_format)

        if dl_min and dl_max:
            return data.filter(deadline_at__range=(dl_min, dl_max))

        if dl_min:
            return data.filter(deadline_at__gt=q_params['dl_min'])

        if dl_max:
            return data.filter(deadline_at__lt=q_params['dl_max'])

        return data

    def tags_filter(self, data, q_params):
        hastags = q_params.get('hastags')

        if hastags:
            tags_ids = q_params['hastags'].split(',')
            return data.filter(tags__in=tags_ids).distinct()

        return data

    def completion_filter(self, data, q_params):
        cmpl_min = q_params.get('completion_min')
        cmpl_max = q_params.get('completion_max')

        if cmpl_min and cmpl_max:
            return data.filter(completion__range=(cmpl_min, cmpl_max))

        if cmpl_min:
            return data.filter(completion__gt=cmpl_min)

        if cmpl_max:
            return data.filter(completion__lt=cmpl_max)

        return data

    def to_representation(self, data=None):
        q_params = self.context['request'].query_params
        date_format = '%Y-%m-%d %H:%M'

        data = self.completion_filter(data, q_params)
        data = self.tags_filter(data, q_params)
        data = self.deadline_range_filter(
            data, q_params, date_format=date_format)

        orderby = q_params.get('order_by')

        if orderby:
            oparams = orderby.split(',')
            for param in oparams:
                if param in self.allow_orderby_params:
                    data = data.order_by(param)

        return super(FilteredTaskSerializer, self).to_representation(data)

    class Meta:
        model = Task
        fields = '__all__'

# class SubtaskSerializer(serializers.ModelSerializer):
#     class Meta:
#         fields = ['id']


class TaskSerializer(serializers.ModelSerializer):
    blocked_by = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    subtasks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    # tags = TaskTagSerializer(many=True)
    # def get_tags(self):
    #     tags = TaskTagSerializer(many=True)

    # blocked_by = serializers.SerializerMethodField(method_name="get_blocked_by")

    class Meta:
        model = Task
        fields = '__all__'
        list_serializer_class = FilteredTaskSerializer


class TodoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoList
        fields = '__all__'
