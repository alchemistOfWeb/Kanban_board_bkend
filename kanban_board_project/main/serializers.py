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
    allow_orderby_params = ['completion', '-completion', 'deadline_at', '-deadline_at']


    tags = TaskTagSerializer(many=True)

    def deadline_range_filter(self, data, q_params, date_format='%Y-%m-%d %H:%M'):        
        dl_min = q_params.get('dl_min')
        dl_max = q_params.get('dl_max')

        if dl_min:
            dl_min = datetime.datetime.strptime(q_params['dl_min'], date_format)

        if dl_max:
            dl_max = datetime.datetime.strptime(q_params['dl_max'], date_format)

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
        data = self.deadline_range_filter(data, q_params, date_format='%Y-%m-%d %H:%M')

        orderby = q_params.get('orderby')
    
        if orderby:
            oparams = q_params['orderby'].split(',')
            for param in oparams:
                if param in self.allow_orderby_params:
                    data = data.order_by(param)

        return super(FilteredTaskSerializer, self).to_representation(data)

    class Meta:
        model = Task
        fields = '__all__'


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

    todo: normal tags field
    """
    # tags = TaskTagSerializer(many=True)
    # def get_tags(self):
    #     tags = TaskTagSerializer(many=True)

    # def create(self, validated_data):
    #     # print("__________________")
    #     # print(validated_data)
    #     return super().create(validated_data)

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
