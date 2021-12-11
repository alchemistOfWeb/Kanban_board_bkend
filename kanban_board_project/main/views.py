from functools import partial
from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, status
from .serializers import TaskSerializer, TodoListSerializer, BoardSerializer, TaskTagSerializer
from .models import Task, TaskTag, TodoList, Board
from kanban_board_project.main import serializers
# from django.db.models.query import QuerySet


# Create your views here.
"""
todo:
 
Board:
* POST:SendInvitations to board to emails
* POST: Create new board
* GET: board users
 
Todolist:
* POST: Create new todolist in board
* GET: board todolists
 
Tasks:
* GET: todolist tasks (with tags, implemented, blockedByIDs, blocks, refersTo, subtaskFor)
* PUT: add tags to task
* PUT: some changes
 
 
Tags:
* POST: Create new tag
* GET: get existing tags
 
Rules:
...
 
User
⇅(boards_users)
Board: title, description
↑
TodoList: title, board(fk MtO)
↑
Task: text, description, status(fk|set), blockedBy(fk MtM>this), subtaskFor(fk MtO>this), todolist(fk MtO)
⇅(tasks_tags)
TaskTag: title
"""


class BoardViewSet(viewsets.ViewSet):
    def list(self, request):
        """
        todo:
        send only user's boards
        get info about tasks of the board
        """
        boards = Board.objects.all()  # todo: filter
        serializer = BoardSerializer(boards, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        data = request.data
        serializer = BoardSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """
        todo:
        get full description of the board
        get info about tasks and todolists of the board
        get todolists with paginated tasks inside
        """
        queryset = Board.objects.all()
        board = get_object_or_404(queryset, pk=pk)
        serializer = BoardSerializer(board)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

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

    def destroy(self, request, pk=None):
        """
        delete board with all its todolists and tasks
        """
        queryset = Board.objects.all()
        board = get_object_or_404(queryset, pk=pk)
        board.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TaskViewSet(viewsets.ViewSet):
    def list(self, request, board_pk=None, todolist_pk=None,):
        """
        get tasks of the board with filtering and pagination
        """
        board = Board.objects.all()
        tasks = board.tasks.all() # todo: filter
        serializer = BoardSerializer(tasks, many=True)        
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def create(self, request, board_pk=None, todolist_pk=None, pk=None):
        """
        create new task in the board
        """
        data = request.data
        serializer = TaskSerializer(data=data)
        if serializer.is_valid():            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, board_pk=None, todolist_pk=None, pk=None):
        """
        get only one task of the todolist
        get subtasks of this task
        """
        queryset = Task.objects.all()
        task = get_object_or_404(queryset, pk=pk)
        serializer = TaskSerializer(task)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, board_pk=None, todolist_pk=None, pk=None):
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

    def partial_update(self, request, board_pk=None, todolist_pk=None, pk=None):
        """
        change some of this: 
        subtasks-list(by ids), 
        blocks(add blockirator, add blocking tasks),
        implementation percentage,
        move into another todolist(by id),
        tags-list(by ids),
        archive|unarchive,
        change the color
        """
        queryset = Task.objects.all()
        task = get_object_or_404(queryset, pk=pk)
        data = request.data
        serializer = TaskSerializer(task, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, board_pk=None, todolist_pk=None, pk=None):
        queryset = Task.objects.all()
        task = get_object_or_404(queryset, pk=pk)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TaskTagViewSet(APIView):
    def list(self, request):
        tags = TaskTag.objects.all()
        serializer = TaskTagSerializer(tags, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        data = request.data
        serializer = BoardSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        queryset = TaskTag.objects.all()
        tag = get_object_or_404(queryset, pk=pk)
        serializer = TaskTagSerializer(tag, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_205_RESET_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        queryset = TaskTag.objects.all()
        tasktag = get_object_or_404(queryset, pk=pk)
        tasktag.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TodoListViewSet(APIView):
    def list(self, request, board_pk=None):
        boards = Board.objects.all()
        board = get_object_or_404(boards, pk=board_pk)
        todolists = board.todolists.all()
        serialized_data = TodoListSerializer(todolists, many=True)
        return Response(serialized_data, status=status.HTTP_200_OK)

    def create(self, request, board_pk=None):
        data = request.data
        serializer = TodoListSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, board_pk=None, pk=None):
        pass

    def update(self, request, board_pk=None, pk=None):
        queryset = TodoList.objects.all()
        todolist = get_object_or_404(queryset, pk=pk)
        serializer = TodoListSerializer(todolist, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_205_RESET_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
        serializer = TodoListSerializer(todolist, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_205_RESET_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, board_pk=None, pk=None):
        queryset = TodoList.objects.all()
        todolist = get_object_or_404(queryset, pk=pk)
        todolist.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
