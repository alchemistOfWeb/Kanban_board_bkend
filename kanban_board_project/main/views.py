from django.shortcuts import get_object_or_404
from django.template import context
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .filters import TaskFilter
from .serializers import TaskSerializer, TodoListSerializer, BoardSerializer, TaskTagSerializer
from .models import Task, TaskTag, TodoList, Board
from .schemas import CustomAutoSchema


class BoardViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    swagger_schema = CustomAutoSchema
    my_tags = ['Boards']
    queryset = Board.objects


    @swagger_auto_schema(operation_description="get list of boards",
                         responses={200: BoardSerializer(many=True)})
    def list(self, request):
        serializer = BoardSerializer(self.queryset, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


    @swagger_auto_schema(operation_description="get list of boards",
                         query_serializer=BoardSerializer,
                         responses={201: BoardSerializer})
    def create(self, request):
        data = request.data
        serializer = BoardSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


    @swagger_auto_schema(operation_description="get one of the boards by id with full info",
                         responses={200: BoardSerializer})
    def retrieve(self, request, pk=None):
        board = get_object_or_404(self.queryset, pk=pk)
        serializer = BoardSerializer(board)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


    @swagger_auto_schema(operation_description="update the board",
                         query_serializer=BoardSerializer)
    def update(self, request, pk=None):
        board = get_object_or_404(self.queryset, pk=pk)
        serializer = BoardSerializer(board, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_205_RESET_CONTENT)


    @swagger_auto_schema(operation_description="partial update the board",
                         query_serializer=BoardSerializer(partial=True))
    def partial_update(self, request, pk=None):
        board = get_object_or_404(self.queryset, pk=pk)
        serializer = BoardSerializer(board, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_205_RESET_CONTENT)


    @swagger_auto_schema(operation_description="delete the board with all its todolists and tasks",
                         responses={204: ""})
    def destroy(self, request, pk=None):
        board = get_object_or_404(self.queryset, pk=pk)
        board.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class TaskViewSet(viewsets.ViewSet):
    queryset = Task.objects
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = TaskFilter
    ordering_fields = ['deadline_at', 'completion']
    permission_classes = [permissions.IsAuthenticated]
    swagger_schema = CustomAutoSchema
    my_tags = ['Tasks']


    def filter_queryset(self, queryset):
        for backend in self.filter_backends:
            queryset = backend().filter_queryset(self.request, queryset, view=self)

        return queryset


    @swagger_auto_schema(operation_description="get the task list with filtering and pagination",
                         responses={200: TaskSerializer(many=True)})
    def list(self, request, board_pk=None):
        tasks = self.queryset.filter(board_id=board_pk)
        serializer = self.serializer_class(self.filter_queryset(tasks), 
                                           many=True, 
                                           context={"request": request})

        return Response(data=serializer.data, status=status.HTTP_200_OK)


    @swagger_auto_schema(operation_description="create new task",
                         query_serializer=TaskSerializer,
                         responses={201: TaskSerializer(many=True)})
    def create(self, request, board_pk=None, pk=None):
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


    @swagger_auto_schema(operation_description="get one of the tasks by id with full info",
                         responses={200: TaskSerializer})
    def retrieve(self, request, board_pk=None, pk=None):
        task = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class(task)

        return Response(serializer.data, status=status.HTTP_200_OK)


    @swagger_auto_schema(operation_description="update the task",
                         query_serializer=TaskSerializer)
    def update(self, request, board_pk=None, pk=None):
        task = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class(task, data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(status=status.HTTP_205_RESET_CONTENT)


    @swagger_auto_schema(operation_description="update the task",
                         query_serializer=TaskSerializer(partial=True))
    def partial_update(self, request, board_pk=None, pk=None):
        task = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class(task, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_205_RESET_CONTENT)


    @swagger_auto_schema(operation_description="delete the task",
                         responses={204: ""})
    def destroy(self, request, board_pk=None, pk=None):
        task = get_object_or_404(self.queryset, pk=pk)
        task.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class TaskTagViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    swagger_schema = CustomAutoSchema
    my_tags = ['Task Tags']
    queryset = TaskTag.objects


    @swagger_auto_schema(operation_description="create new task tag",
                         responses={200: TaskTagSerializer(many=True)})
    def list(self, request):
        serializer = TaskTagSerializer(self.queryset, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


    @swagger_auto_schema(operation_description="create new task tag",
                         query_serializer=TaskTagSerializer,
                         responses={201: TaskTagSerializer})
    def create(self, request):
        data = request.data
        serializer = TaskTagSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


    @swagger_auto_schema(operation_description="update the task",
                         query_serializer=TaskTagSerializer,
                         responses={205: TaskTagSerializer})
    def update(self, request, pk=None):
        tag = get_object_or_404(self.queryset, pk=pk)
        serializer = TaskTagSerializer(tag, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_205_RESET_CONTENT)


    @swagger_auto_schema(operation_description="update the task",
                         query_serializer=TaskTagSerializer(partial=True),
                         responses={205: TaskTagSerializer})
    def partial_update(self, request, pk=None):
        tag = get_object_or_404(self.queryset, pk=pk)
        serializer = TaskTagSerializer(tag, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_205_RESET_CONTENT)


    @swagger_auto_schema(operation_description="delete the task tag",
                         responses={204: ""})
    def destroy(self, request, pk=None):
        tasktag = get_object_or_404(self.queryset, pk=pk)
        tasktag.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class TodoListViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    swagger_schema = CustomAutoSchema
    my_tags = ['Todolists']
    queryset = TodoList.objects


    @swagger_auto_schema(operation_description="update the board",
                         responses={200: TodoListSerializer(many=True)})
    def list(self, request, board_pk=None):
        todolists = TodoList.objects.filter(board_id=board_pk)
        serializer = TodoListSerializer(todolists, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


    @swagger_auto_schema(operation_description="create new todolist",
                         query_serializer=TodoListSerializer)
    def create(self, request, board_pk=None):
        data = request.data
        serializer = TodoListSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


    @swagger_auto_schema(operation_description="update the todolist",
                         query_serializer=TodoListSerializer)
    def update(self, request, board_pk=None, pk=None):
        todolist = get_object_or_404(self.queryset, pk=pk)
        serializer = TodoListSerializer(todolist, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_205_RESET_CONTENT)


    @swagger_auto_schema(operation_description="partial update the todolist",
                         query_serializer=TodoListSerializer(partial=True))
    def partial_update(self, request, board_pk=None, pk=None):
        todolist = get_object_or_404(self.queryset, pk=pk)
        serializer = TodoListSerializer(
            todolist, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_205_RESET_CONTENT)


    @swagger_auto_schema(operation_description="delete the todolist",
                         responses={204: ""})
    def destroy(self, request, board_pk=None, pk=None):
        todolist = get_object_or_404(self.queryset, pk=pk)
        todolist.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
