from . import views
from django.urls import path


app_name = 'blog'
urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('new/', views.post_new, name='post_create'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail'),
    path('update/<slug:slug>/', views.PostUpdateView.as_view(), name='post-update'),
    path('delete/<slug:slug>/', views.PostDeleteView.as_view(), name='post-delete'),
    path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),
    path('search/', views.SearchResultsView.as_view(), name='search_results'),
]
