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
    tags = TaskTagSerializer(many=True)
    

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
