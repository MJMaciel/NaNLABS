from django.urls import path

from .views import task_creator


urlpatterns = [
    path('', task_creator, name='task-list'),
]