from django.contrib.auth import get_user_model
# from django.core.mail import send_mail
from todo import settings
from celery import shared_task
from django.core.mail import send_mail
from todo import settings
from .models import Task
from django.utils import timezone

@shared_task(bind=True)
def send_mail_to_assigned_user(self, task_id,user_email):
    print(task_id, 'task_id')
    send_mail(
        subject='Test Mail',
        message='This is a test mail',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user_email],
        fail_silently=True,
    )
    return 'Email Sent Successfully'

@shared_task(bind=True)
def send_mail_if_deadline_passed(self, task_id, user_email):
    try:
        task = Task.objects.get(id=task_id)
        if task.deadline < timezone.now() and task.status == 'pending':
            print('i Sending Email...')
            send_mail(
                subject='Task Deadline Passed',
                message='The deadline for the task has passed and it is still pending.',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user_email],
                fail_silently=True,
            )
            print('Sending Email...')
            return 'Email Sent Successfully'
        return 'Task is not pending or deadline not passed'
    except Task.DoesNotExist:
        return 'Task does not exist'


# also add a celery beat schedule to send mail, if the task deadline is passed and the task is not completed.