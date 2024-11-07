from django.urls import path
from .views import home_page_view, todo_detail_view, is_done_view, is_active_view, update_todo_view, add_new_todo_view, delete_todo_view


urlpatterns = [
    path('', home_page_view, name='home'),
    path('todo-detail/<slug:slug>/', todo_detail_view, name='todo-detail'),
    path('is-done/<int:pk>/', is_done_view, name='is-done'),
    path('is-active/<int:pk>/', is_active_view, name='is-active'),
    path('todo-update/<slug:slug>/', update_todo_view, name='todo-update'),
    path('add-todo/', add_new_todo_view, name='add-todo'),
    path('todo-delete/<slug:slug>/', delete_todo_view, name='delete-todo'),
]