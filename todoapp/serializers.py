from rest_framework import serializers
from .models import Task, Profile
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])
        return user

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        exclude = ('created_at', 'updated_at')
        

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
        

#TODO JWT, MIDDLEWARE, ALSO HAD TO BE IMPLEMENTED