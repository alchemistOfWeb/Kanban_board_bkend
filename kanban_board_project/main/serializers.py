from rest_framework import serializers
from .models import Board, Task, TodoList, TaskTag
import datetime


class BoardSerializer(serializers.ModelSerializer):
    """ 
    fields:
    {
        title: Char(255),
        description: Text(2048),
        created_at: auto,
        updated_at: auto,
        users_ids: [3, 4, 8],
    }
    """
    class Meta:
        model = Board
        fields = '__all__'


class TaskTagSerializer(serializers.ModelSerializer):
    """ 
    fields:
    {
        title: Char(255, unique),
    }
    """
    class Meta:
        model = TaskTag
        fields = '__all__'


class FilteredTaskSerializer(serializers.ListSerializer):
    """
    # completed=True/False
    # &

    deadline_range between date1 and date2[x]
    &
    order_by start_at or deadline_at[ ] and order_by completion
    &
    has tags in tags_array[x]
    &
    is_archive
    &
    completion between degree1 and degree2


    """

    def to_representation(self, data):
        q_params = self.context['request'].query_params

        date_format = '%d-%m-%Y %H:%M:%S'
        deadline_range = (
            datetime.datetime.strptime(
                q_params['deadline_range'][0], date_format),
            datetime.datetime.strptime(
                q_params['deadline_range'][1], date_format)
        )

        data = data\
            .filter(tags__id__in=q_params['hastags'])\
            .filter(deadline_at__range=deadline_range)\
            .order_by('completion')

        return super(FilteredTaskSerializer, self).to_representation(data)


class TaskSerializer(serializers.ModelSerializer):
    """ 
    fields:
    {
        title: Char(255),
        start_at: datetime,
        deadline_at: datetime,
        completion: float(0-100),
        board: id,
        todolist: id,
        position: integer
    }  
    """
    tags = TaskTagSerializer(many=True)

    # blocks = BlockTaskListSerializer(many=True)

    # blocked_by = serializers.SerializerMethodField(method_name="get_blocked_by")

    # def get_blocked_by(self, obj):
    #     obj.blocked_by
    #     return
    class Meta:
        model = Task
        fields = '__all__'
        list_serializer_class = FilteredTaskSerializer


class TodoListSerializer(serializers.ModelSerializer):
    """
    create,
    get,
    update,
    delete
    """

    class Meta:
        model = TodoList
        fields = '__all__'
