from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register('boards/<int:board_pk>/tasks', views.TaskViewSet, basename='tasks')
router.register('boards', views.BoardViewSet, basename='boards')
router.register('tags', views.TaskTagViewSet, basename='tags')
router.register('boards/<int:board_pk>todolists', views.TodoListViewSet, basename='todolists')

urlpatterns = [] + router.urls
