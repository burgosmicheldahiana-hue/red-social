from django.urls import path
from . import views

urlpatterns = [
    path("feed/", views.FeedView.as_view(), name="api-feed"),
    path("", views.PostListCreateView.as_view(), name="api-post-list"),
    path("<int:pk>/", views.PostDetailView.as_view(), name="api-post-detail"),
    path("<int:pk>/like/", views.like_toggle, name="api-like-toggle"),
    path("<int:pk>/comments/", views.CommentListCreateView.as_view(), name="api-comment-list"),
]
