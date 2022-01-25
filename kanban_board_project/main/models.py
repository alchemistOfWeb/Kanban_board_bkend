from datetime import timezone
from django.db import models
from colorfield.fields import ColorField
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


class Board(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=2048)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    users = models.ManyToManyField(User, related_name='boards')


    def __str__(self) -> str:
        return self.title


class TodoList(models.Model):
    title = models.CharField(max_length=255)
    position = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_archived = models.BooleanField(default=False)
    archived_at = models.DateTimeField(null=True)

    board = models.ForeignKey(
        'board', related_name='todolists', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.title


class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=1024)
    color = ColorField(default='#FF0000', null=True)
    completion = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(100)], default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    start_at = models.DateTimeField(null=True, blank=True)
    deadline_at = models.DateTimeField(null=True, blank=True)

    board = models.ForeignKey(
        'Board', related_name='tasks', on_delete=models.CASCADE, null=True)
    todo_list = models.ForeignKey(
        'TodoList', on_delete=models.CASCADE, null=True, related_name='tasks')
    tags = models.ManyToManyField('TaskTag', related_name='tasks', blank=True)

    blocks_tasks = models.ManyToManyField(
        'Task', related_name='blocked_by', blank=True)

    subtask_for = models.ForeignKey(
        'Task',
        related_name='subtasks',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self) -> str:
        return self.title

    # refers_to = models.ForeignKey(
    #                               'Task',
    #                               related_name='refs',
    #                               on_delete=models.SET_NULL,
    #                               null=True
    #                               )


class TaskTag(models.Model):
    title = models.CharField(max_length=255, unique=True)
    color = ColorField(default='#FF0000')

    def __str__(self) -> str:
        return self.title
