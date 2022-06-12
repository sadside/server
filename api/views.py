from inspect import stack
from django.shortcuts import redirect
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import ToDoSerializer, UserSerializer, EditToDoSerializer
from .models import ToDo
from django.contrib.auth.models import User


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_user_data(request):
    todos = ToDo.objects.filter(owner=request.user)
    done_todos = todos.filter(is_done=True)

    answer = {
        "id": request.user.id,
        "username": request.user.username,
        "email": request.user.email,
        "todos_count": len(todos),
        "done_todo_count": len(done_todos),
        "not_done_to_count": len(todos) - len(done_todos),
    }

    return Response(answer, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def todo_list(request):
    if request.method == "GET":
        todo = ToDo.objects.filter(owner=request.user)
        serializer = ToDoSerializer(todo, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = ToDoSerializer(data=request.data)

        serializer.initial_data["owner_id"] = request.user.id

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "DELETE", "PUT"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def todo_detail(request, pk: int):
    try:
        todo = ToDo.objects.get(pk=pk, owner=request.user)
    except ToDo.DoesNotExist:
        return Response(status.HTTP_404_NOT_FOUND)

    print(todo)

    if request.method == "GET":
        serializer = ToDoSerializer(todo)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = EditToDoSerializer(todo, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        todo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    return Response(status=status.HTTP_400_BAD_REQUEST)
