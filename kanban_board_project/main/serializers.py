from rest_framework import serializers
from .models import Board, Task, TodoList, TaskTag
 
 
class BoardSerializer(serializers.ModelSerializer):
    """
    BoardSerializer(queryset_obj) :retrieve
    BoardSerializer(queryset_obj, many) :list
    BoardSerializer(data=validated_data) :create
    BoardSerializer(data=validated_data) :update
    BoardSerializer(data=validated_data) :partial_update
    obj(pk).delete() :destroy
 
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
    BoardSerializer(queryset_obj) :retrieve
    BoardSerializer(queryset_obj, many) :list
    BoardSerializer(data=validated_data) :create
    BoardSerializer(data=validated_data) :update
    obj(pk).delete() :destroy
 
    fields:
    {
        title: Char(255, unique),
    }
    """
    class Meta:
        model = TaskTag
        fields = '__all__'
 
 
class TaskSerializer(serializers.ModelSerializer):
    """
    BoardSerializer(queryset_obj) :retrieve
    BoardSerializer(queryset_obj, many) :list
    BoardSerializer(data=validated_data) :create
    BoardSerializer(data=validated_data) :update
    BoardSerializer(data=validated_data) :partial_update (add tag, change position, move to another todolist...)
    obj(pk).delete() :destroy
 
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
