from django.urls import path
from . import views

urlpatterns = [
    path('get_blogs/', views.task_list.as_view(), name='task-list'),
]