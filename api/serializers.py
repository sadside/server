from pkg_resources import require
from rest_framework import serializers
from django.contrib.auth.models import User

from .models import ToDo


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email')


class ToDoSerializer(serializers.HyperlinkedModelSerializer):
    owner_id = serializers.IntegerField()

    class Meta:
        model = ToDo
        fields = ('id', 'text', 'is_done', 'owner_id')

class EditToDoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ToDo
        fields = ('id', 'text', 'is_done')
