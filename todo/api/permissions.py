from rest_framework.permissions import BasePermission

class IsTodoOwner(BasePermission):
    '''Permission to check if current logged in user is the owner of the todo'''
    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner