from datetime import timezone
from django.db import models
from colorfield.fields import ColorField
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
"""
todo:

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
 
class Board(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=2048)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
 
    users = models.ManyToManyField(User, related_name='boards')
    # creator = models.ForeignKey(User, related_name='ownboards')
 
 
class TodoList(models.Model):
    title = models.CharField(max_length=255)
    position = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_archived = models.BooleanField(default=False)
    archived_at = models.DateTimeField(null=True) # need for deleting after some time
 
    board = models.ForeignKey('board', related_name='todolists', on_delete=models.CASCADE)
 
 
class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=1024)
    color = ColorField(default='#FF0000', null=True)
    completion = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)], default=0)
    created_at = models.DateTimeField(auto_now_add=True,)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True)
    start_at = models.DateTimeField(null=True)
    deadline_at = models.DateTimeField(null=True)

    board = models.ForeignKey('Board', related_name='tasks', on_delete=models.CASCADE, null=True)
    todo_list = models.ForeignKey('TodoList', on_delete=models.CASCADE, null=True)
    tags = models.ManyToManyField('TaskTag', related_name='tasks')
    blocks_tasks = models.ManyToManyField('Task', related_name='blocked_by') # мы не можем приступить к выполнению блокируемой задачи пока не решим все задачи-блокираторы (устанавливается определённый порядок выполнения)
    subtask_for = models.ForeignKey(
                                    'Task',
                                    related_name='subtasks',
                                    on_delete=models.SET_NULL,
                                    null=True
                                    ) # обычно одну сложную задачу разбивают на более простые и мелкие подзадачи
    # refers_to = models.ForeignKey(
    #                               'Task',
    #                               related_name='refs',
    #                               on_delete=models.SET_NULL,
    #                               null=True
    #                               ) # от выполнения одной задачи зависит и выполнение второй (выполняются в любом порядке)
   
 
class TaskTag(models.Model):
    title = models.CharField(max_length=255, unique=True)
    color = ColorField(default='#FF0000')
 
 
# class TaskStatus(models.)
