from django.shortcuts import get_object_or_404
from django_filters.filters import OrderingFilter
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, status, permissions
from .serializers import TaskSerializer, TodoListSerializer, BoardSerializer, TaskTagSerializer
from .models import Task, TaskTag, TodoList, Board
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .schemas import CustomAutoSchema


class BoardViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    swagger_schema = CustomAutoSchema
    my_tags = ['Boards']
    qeuryset = Board.objects


    @swagger_auto_schema(operation_description="get list of boards",
                         responses={200: BoardSerializer(many=True)})
    def list(self, request):
        """
        todo:
        send only user's boards
        get info about tasks of the board (num, last update,...)
        """
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
    # filter_backends = (DjangoFilterBackend, OrderingFilter)
    # ordering_fields = ['deadline_at', 'position', 'completion']
    permission_classes = [permissions.IsAuthenticated]
    swagger_schema = CustomAutoSchema
    my_tags = ['Tasks']
    queryset = Task.objects


    @swagger_auto_schema(operation_description="get the task list with filtering and pagination",
                         manual_parameters=[
                             openapi.Parameter(
                                 'dl_min', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING, pattern='%Y-%m-%d %H:%M'),
                             openapi.Parameter(
                                 'dl_max', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING,
                                 pattern='%Y-%m-%d %H:%M'),
                             openapi.Parameter(
                                 'hastags', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING, pattern='int1,int2...'),
                             openapi.Parameter(
                                 'completion_min', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
                             openapi.Parameter(
                                 'completion_max', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
                             openapi.Parameter('order_by', in_=openapi.IN_QUERY, 
                                 type=openapi.TYPE_STRING, 
                                 pattern='str1[,str2[, ...]',
                                 description='order by parameter. It can be completion or -completion, deadline or -deadline'),
                         ],
                         responses={200: TaskSerializer(many=True)})
    def list(self, request, board_pk=None):
        tasks = Task.objects.filter(board_id=board_pk)
        serializer = TaskSerializer(
            tasks, many=True, context={'request': request})

        return Response(data=serializer.data, status=status.HTTP_200_OK)


    @swagger_auto_schema(operation_description="create new task",
                         query_serializer=TaskSerializer,
                         responses={201: TaskSerializer(many=True)})
    def create(self, request, board_pk=None, pk=None):
        data = request.data
        serializer = TaskSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


    @swagger_auto_schema(operation_description="get one of the tasks by id with full info",
                         responses={200: TaskSerializer})
    def retrieve(self, request, board_pk=None, pk=None):
        task = get_object_or_404(self.queryset, pk=pk)
        serializer = TaskSerializer(task)

        return Response(serializer.data, status=status.HTTP_200_OK)


    @swagger_auto_schema(operation_description="update the task",
                         query_serializer=TaskSerializer)
    def update(self, request, board_pk=None, pk=None):
        task = get_object_or_404(self.queryset, pk=pk)
        serializer = TaskSerializer(task, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_205_RESET_CONTENT)

        return Response(status=status.HTTP_400_BAD_REQUEST)


    @swagger_auto_schema(operation_description="update the task",
                         query_serializer=TaskSerializer(partial=True))
    def partial_update(self, request, board_pk=None, pk=None):
        task = get_object_or_404(self.queryset, pk=pk)
        serializer = TaskSerializer(task, data=request.data, partial=True)
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
