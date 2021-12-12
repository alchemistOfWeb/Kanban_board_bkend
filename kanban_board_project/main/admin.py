from django.contrib import admin
from .models import Task, TaskTag, TodoList, Board


# class TaskAdmin(admin.ModelAdmin):


admin.site.register(Task)
admin.site.register(TaskTag)
admin.site.register(TodoList)
admin.site.register(Board)

# Register your models here.
