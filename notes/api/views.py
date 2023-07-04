from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework import status
from rest_framework.exceptions import NotFound

from .serializers import NoteSerializer, UpdateNoteSerializer
from notes.models import Note
from .permissions import IsNoteAuthor

# Create your views here.
class UserNoteListView(generics.ListAPIView):

    '''View to access notes of current logged in user'''

    serializer_class = NoteSerializer

    def get_queryset(self):
        # get current user
        current_user = self.request.user

        # filter based on current user
        return Note.objects.filter(author=current_user)
    
    def list(self, request, *args, **kwargs):
        # get current_user
        current_user = self.request.user

        # queryset
        notes = Note.objects.filter(author=current_user)

        # serializer
        serializer = self.serializer_class(notes, many=True)

        if not notes.exists():
            return Response({'message':'You have no notes yet. Create one.'})
        
        return Response(serializer.data)
    

class NoteCreateView(generics.CreateAPIView):

    '''Note creation view'''

    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]
    queryset = Note.objects.all()

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class NoteDetailsView(generics.RetrieveUpdateDestroyAPIView):

    '''View to get, update and delete note item'''
    
    serializer_class = UpdateNoteSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsNoteAuthor]

    def get(self, request, *args, **kwargs):

        '''get function to check if a note exists or not'''
        
        pk = self.kwargs['pk']

        try:
            note = Note.objects.get(pk=pk)
            serializer = self.serializer_class(note)
            return Response(serializer.data)
        except Note.DoesNotExist:
            return Response({'error': 'Note does not exist'})
    
    def get_object(self):
        pk = self.kwargs['pk']
        note = Note.objects.get(pk=pk)
        self.check_object_permissions(self.request, note)
        return note
    
    def delete(self, request, *args, **kwargs):
        try:
            pk = self.kwargs['pk']
            note = Note.objects.get(pk=pk)
            super().delete(request, *args, **kwargs)
            return Response({'message': f'Note {note.title} deleted.'})
        except Note.DoesNotExist:
            raise NotFound('Note does not exist')