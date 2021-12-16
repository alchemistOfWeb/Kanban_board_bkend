from django.shortcuts import render, get_object_or_404
from django_filters.filters import OrderingFilter
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, status, permissions
from .serializers import TaskSerializer, TodoListSerializer, BoardSerializer, TaskTagSerializer
from .models import Task, TaskTag, TodoList, Board
# from django.db.models.query import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from django.utils.decorators import method_decorator
from drf_yasg.inspectors import SwaggerAutoSchema
from drf_yasg import openapi


class CustomAutoSchema(SwaggerAutoSchema):

    def get_tags(self, operation_keys=None):
        tags = self.overrides.get('tags', None) or getattr(
            self.view, 'my_tags', [])
        if not tags:
            tags = [operation_keys[0]]

        return tags


class BoardViewSet(viewsets.ViewSet):
    """
    # Boards
    """
    permission_classes = [permissions.IsAuthenticated]
    swagger_schema = CustomAutoSchema
    my_tags = ['Boards']
    # filter_backends =
    # permission_classes_by_action = {'list': [permissions.IsAuthenticated], 'retrieve': [permissions.IsAuthenticated]}

    @swagger_auto_schema(operation_description="get list of boards",
                         responses={200: BoardSerializer(many=True)})
    def list(self, request):
        """
        todo:
        send only user's boards
        get info about tasks of the board
        """
        boards = Board.objects.all()  # todo: filter
        serializer = BoardSerializer(boards, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    
    @swagger_auto_schema(operation_description="get list of boards",
                         query_serializer=BoardSerializer,
                         responses={201: BoardSerializer})
    def create(self, request):
        data = request.data
        serializer = BoardSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(operation_description="get one of the boards by id with full info", 
                         responses={200: BoardSerializer})
    def retrieve(self, request, pk=None):
        """
        todo:
        get full description of the board
        get info about tasks and todolists of the board (tasks/todolists count,)
        get todolists with paginated tasks inside
        """
        queryset = Board.objects.all()
        board = get_object_or_404(queryset, pk=pk)
        serializer = BoardSerializer(board)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(operation_description="update the board",
                         query_serializer=BoardSerializer)
    def update(self, request, pk=None):
        """
        change all: board name, board description, board users
        """
        queryset = Board.objects.all()
        board = get_object_or_404(queryset, pk=pk)
        serializer = BoardSerializer(board, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_205_RESET_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(operation_description="update the board",
                         query_serializer=BoardSerializer(partial=True))
    def partial_update(self, request, pk=None):
        """
        change some of this: board name, board description, board users
        """
        queryset = Board.objects.all()
        board = get_object_or_404(queryset, pk=pk)
        serializer = BoardSerializer(board, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_205_RESET_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(operation_description="delete the board",
                         responses={204: ""})
    def destroy(self, request, pk=None):
        """
        delete board with all its todolists and tasks
        """
        queryset = Board.objects.all()
        board = get_object_or_404(queryset, pk=pk)
        board.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TaskViewSet(viewsets.ViewSet):
    # filter_backends = (DjangoFilterBackend, OrderingFilter)
    # ordering_fields = ['deadline_at', 'position', 'completion']
    permission_classes = [permissions.IsAuthenticated]
    swagger_schema = CustomAutoSchema
    my_tags = ['Tasks']

    @swagger_auto_schema(operation_description="get the task list with filtering and pagination",
                         manual_parameters=[
                            openapi.Parameter('dl_min', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING, pattern='%Y-%m-%d %H:%M'),
                            openapi.Parameter('dl_max', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING,
                            pattern='%Y-%m-%d %H:%M'),
                            openapi.Parameter('hastags', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING, pattern='int1,int2...'),
                            openapi.Parameter('completion_min', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
                            openapi.Parameter('completion_max', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
                         ],
                        #  request_body=openapi.Schema(
                        #      type=openapi.TYPE_OBJECT,
                        #      properties={
                        #          'dl_min': openapi.Schema(type=openapi.IN_QUERY, ),
                        #          'dl_min': openapi.Schema(),
                        #          'dl_min': openapi.Schema(),
                        #          'dl_min': openapi.Schema(),
                        #          'dl_min': openapi.Schema(),
                        #      }),
                         responses={200: TaskSerializer(many=True)})
    def list(self, request, board_pk=None):
        """
        get tasks of the board with filtering and pagination
        """
        queryset = Board.objects.all()
        board = get_object_or_404(queryset, pk=board_pk)
        # q_params = request.query_params
        tasks = board.tasks.all()

        serializer = TaskSerializer(
            tasks, many=True, context={'request': request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(operation_description="create new task",
                         query_serializer=TaskSerializer,
                         responses={201: TaskSerializer(many=True)})
    def create(self, request, board_pk=None, pk=None):
        """
        create new task in the board
        """
        data = request.data
        serializer = TaskSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(operation_description="get one of the tasks by id with full info", 
                         responses={200: TaskSerializer})
    def retrieve(self, request, board_pk=None, pk=None):
        """
        get only one task of the todolist
        get subtasks of this task
        """
        queryset = Task.objects.all()
        task = get_object_or_404(queryset, pk=pk)
        serializer = TaskSerializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(operation_description="update the task",
                         query_serializer=TaskSerializer)
    def update(self, request, board_pk=None, pk=None):
        """
        change
        """
        queryset = Task.objects.all()
        task = get_object_or_404(queryset, pk=pk)
        data = request.data
        serializer = TaskSerializer(task, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(operation_description="update the task",
                         query_serializer=TaskSerializer(partial=True))
    def partial_update(self, request, board_pk=None, pk=None):
        queryset = Task.objects.all()
        task = get_object_or_404(queryset, pk=pk)
        data = request.data
        serializer = TaskSerializer(task, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(operation_description="delete the task",
                         responses={204: ""})
    def destroy(self, request, board_pk=None, pk=None):
        queryset = Task.objects.all()
        task = get_object_or_404(queryset, pk=pk)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TaskTagViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    swagger_schema = CustomAutoSchema
    my_tags = ['Task Tags']

    @swagger_auto_schema(operation_description="create new task tag",                         
                         responses={200: TaskTagSerializer(many=True)})
    def list(self, request):
        tags = TaskTag.objects.all()
        serializer = TaskTagSerializer(tags, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(operation_description="create new task tag",
                         query_serializer=TaskTagSerializer,
                         responses={201: TaskTagSerializer})
    def create(self, request):
        """
        {
            "title": "unique tag name",
            "color": "#ff0000"
        }
        """
        data = request.data
        serializer = TaskTagSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(operation_description="update the task",
                         query_serializer=TaskTagSerializer,
                         responses={205: TaskTagSerializer})
    def update(self, request, pk=None):
        queryset = TaskTag.objects.all()
        tag = get_object_or_404(queryset, pk=pk)
        serializer = TaskTagSerializer(tag, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_205_RESET_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(operation_description="update the task",
                         query_serializer=TaskTagSerializer(partial=True),
                         responses={205: TaskTagSerializer})
    def partial_update(self, request, pk=None):
        queryset = TaskTag.objects.all()
        tag = get_object_or_404(queryset, pk=pk)
        serializer = TaskTagSerializer(tag, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_205_RESET_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(operation_description="delete the task tag",
                         responses={204: ""})
    def destroy(self, request, pk=None):
        queryset = TaskTag.objects.all()
        tasktag = get_object_or_404(queryset, pk=pk)
        tasktag.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TodoListViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    swagger_schema = CustomAutoSchema
    my_tags = ['Todolists']

    @swagger_auto_schema(operation_description="update the board",
                         responses={200: TodoListSerializer(many=True)})
    def list(self, request, board_pk=None):
        queryset = Board.objects.all()
        board = get_object_or_404(queryset, pk=board_pk)
        todolists = board.todolists.all()
        serializer = TodoListSerializer(todolists, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(operation_description="create new todolist",
                         query_serializer=TodoListSerializer)
    def create(self, request, board_pk=None):
        data = request.data
        serializer = TodoListSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def retrieve(self, request, board_pk=None, pk=None):
    #     pass

    @swagger_auto_schema(operation_description="update the todolist",
                         query_serializer=TodoListSerializer)
    def update(self, request, board_pk=None, pk=None):
        queryset = TodoList.objects.all()
        todolist = get_object_or_404(queryset, pk=pk)
        serializer = TodoListSerializer(todolist, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_205_RESET_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(operation_description="partial update the todolist",
                         query_serializer=TodoListSerializer(partial=True))
    def partial_update(self, request, board_pk=None, pk=None):
        """
        change some of this:
        move position(new pos int)
        title,
        archive|unarchive,
        # move all tasks into another todolist
        """
        queryset = TodoList.objects.all()
        todolist = get_object_or_404(queryset, pk=pk)
        serializer = TodoListSerializer(
            todolist, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_205_RESET_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(operation_description="delete the todolist",
                         responses={204: ""})
    def destroy(self, request, board_pk=None, pk=None):
        queryset = TodoList.objects.all()
        todolist = get_object_or_404(queryset, pk=pk)
        todolist.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
