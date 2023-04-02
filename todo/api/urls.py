from django.urls import path
from . import views 

urlpatterns = [
    path('list/', views.UserTodoListGV.as_view(), name='user-todo-list'),
    path('list/create/', views.TodoCreateView.as_view(), name='todo-create'),
    path('list/<int:pk>/', views.TodoItemView.as_view(), name='todo-item'),
]