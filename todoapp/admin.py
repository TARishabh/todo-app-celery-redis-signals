from django.contrib import admin
from .models import Profile,Task,Analytics
from django.contrib.auth.models import User


# Register your models here.

# admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Task)
admin.site.register(Analytics)