from django.shortcuts import render
from rest_framework.views import APIView


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


class Board(APIView):
    def post(self, request, pk, format=None):
        ...


    def get(self, request, pk, format=None):
        ...


    def put(self, request, pk, format=None):
        ...

    
    def delete(self, request, pk, format=None):
        ...

    
