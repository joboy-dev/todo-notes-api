from rest_framework.permissions import BasePermission

class IsNoteAuthor(BasePermission):
    '''Permission to check if current logged in user is the author of the note'''
    def has_object_permission(self, request, view, obj):
        return request.user == obj.author