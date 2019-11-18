from . import views
from django.urls import path


app_name = 'comments'
urlpatterns = [
    path('<int:id>/', views.comment_thread, name='thread'),
    path('delete/<int:id>/', views.comment_delete, name='delete'),
]
