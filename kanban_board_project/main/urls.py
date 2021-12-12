from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register('boards', views.BoardViewSet, basename='boards')
router.register('tags', views.TaskTagViewSet, basename='tags')
router.register(r'boards/(?P<board_pk>\d+)/tasks', views.TaskViewSet, basename='tasks')
router.register(r'boards/(?P<board_pk>\d+)/todolists', views.TodoListViewSet, basename='todolists')

urlpatterns = [] + router.urls
