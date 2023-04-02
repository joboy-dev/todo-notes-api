from django.urls import path
from . import views

app_name = 'notes'
urlpatterns = [
    path('list/', views.UserNoteListView.as_view(), name='note-list'),
    path('create/', views.NoteCreateView.as_view(), name='note-create'),
    path('list/<int:pk>/', views.NoteDetailsView.as_view(), name='note-details'),
]