from django.db import models
from colorfield.fields import ColorField
from django.db.models.fields import CharField, FloatField
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

    users = models.ManyToManyField(User, related_name='boards')
    # creator = models.ForeignKey(User, related_name='ownboards')


class TodoList(models.Model):
    title = models.CharField(max_length=255)
    position = models.IntegerField()
    is_archived = models.BooleanField(default=False)

    board = models.ForeignKey('board', on_delete=models.CASCADE)


class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=1024)
    color = ColorField(default='#FF0000')
    completion = FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)], default=0)

    todo_list = models.ForeignKey('TodoList', on_delete=models.PROTECT)
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
    title = models.CharField(max_length=255)
    color = ColorField(default='#FF0000')


# class TaskStatus(models.)
