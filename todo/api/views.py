from django.shortcuts import render

from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from todo.models import Todo
from .serializers import TodoSerializer, UpdateTodoSerializer
from .permissions import IsTodoOwner


# view to get user to do list. no need for getting primary key value
class UserTodoListGV(generics.ListAPIView):

    '''View to access todo items of current logged in user'''

    serializer_class = TodoSerializer

    def get_queryset(self):
        # get surrent user
        current_user = self.request.user

        # filter based on current user
        user_todos = Todo.objects.filter(owner=current_user)
        
        # return all items
        return user_todos
    
    # overriding the list method to have a custom response if there is no data and to GET the list of todo items
    # treat like a def get() function
    def list(self, request, *args, **kwargs):

        current_user = self.request.user

        user_todos = Todo.objects.filter(owner=current_user)

        # get serializer data and store it
        serializer = self.serializer_class(user_todos, many=True)

        # check if there are todo items in user list
        if not user_todos.exists():
            return Response({'message': 'You have no todos available. Create one.'})
        
        return Response(serializer.data)
    
    
class TodoCreateView(generics.CreateAPIView):

    '''Todo creation view'''

    serializer_class = TodoSerializer
    permission_classes = [IsAuthenticated]
    queryset = Todo.objects.all()
        
    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class TodoItemView(generics.RetrieveUpdateDestroyAPIView):

    '''View to get, update and delete todo item'''

    serializer_class = UpdateTodoSerializer
    permission_classes = [IsAuthenticated, IsTodoOwner]

    def get(self, request, *args, **kwargs):

        '''get function to check if a todo item exists or not'''
        
        pk = self.kwargs['pk']

        try:
            todo = Todo.objects.get(pk=pk)
            serializer = self.serializer_class(todo)
            return Response(serializer.data)
        except Todo.DoesNotExist:
            return Response({'error': 'Todo does not exist'})
            
    def get_object(self):
        pk = self.kwargs['pk']
        todo = Todo.objects.get(pk=pk)
        self.check_object_permissions(self.request, todo)
        return todo
