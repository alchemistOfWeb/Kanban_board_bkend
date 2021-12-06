from django.db import models

"""
todo:

ProjectBoard
^
TodoList
^
Task: text, description, status(fk|set), blockedBy(fk MtM>this), subtaskFor(fk MtO>this)
^
TaskTag: title
"""


