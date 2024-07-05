from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from .serializers import UserSerializer,TaskSerializer
from .tasks import send_mail_to_assigned_user,send_mail_if_deadline_passed
from .models import Task
from rest_framework import status
from django.core.cache import cache
from django_celery_beat.models import PeriodicTask,CrontabSchedule
from uuid import uuid4 
import json


class UserViewSet(
    ListModelMixin, CreateModelMixin, RetrieveModelMixin, 
    UpdateModelMixin, DestroyModelMixin, GenericViewSet
):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    authentication_classes = []

    def get_queryset(self):
        # deadline_call.delay()
        return super().get_queryset()
    
    def get_object(self):
        return super().get_object()
    
# whenever someone creates or assigns a task, a mail should be sent to the user.
class TaskViewSet(ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        if response.status_code == status.HTTP_201_CREATED:
            task_id = response.data['id']
            user_email = User.objects.get(id=response.data['assigned_user']).email
            send_mail_to_assigned_user.delay(task_id, user_email)
            
            date_time_list = response.data['deadline'].split('T')
            schedule, created = CrontabSchedule.objects.get_or_create(
                hour=date_time_list[1].split(':')[0],
                minute=date_time_list[1].split(':')[1],
            )
            task = PeriodicTask.objects.create(
                crontab=schedule,
                name=f'Send Mail if Deadline Passed {uuid4()}',  # keep this unique
                task='todoapp.tasks.send_mail_if_deadline_passed',
                args=json.dumps([task_id, user_email]),  # convert to JSON string
            )
            
        return response

    def get_queryset(self):
        cached_data = cache.get('tasks')
        if cached_data is None:
            tasks = super().get_queryset()
            data = cache.set('tasks', tasks, 60)
            print('cache is None, coming from db')
        else:
            print('cache is not None, coming from cache')
            data = cached_data
        return data
    
    def get_object(self):
        return super().get_object()




