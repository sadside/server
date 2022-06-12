from django.urls import path, include, re_path
from rest_framework.authtoken.views import obtain_auth_token

from . import views


urlpatterns = [
    path('todo/', views.todo_list, name="todo_list"),
    path('todo/<int:pk>', views.todo_detail, name="todo_detail"),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    path('get-user-data/', views.get_user_data, name="get_user_data"),
]
