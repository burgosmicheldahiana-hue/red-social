from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

urlpatterns = [
    path("register/", views.RegisterView.as_view(), name="api-register"),
    path("login/", TokenObtainPairView.as_view(), name="api-login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="api-token-refresh"),

    path("me/", views.ProfileView.as_view(), name="api-profile"),
    path("", views.UserListView.as_view(), name="api-user-list"),
    path("<str:username>/", views.UserDetailView.as_view(), name="api-user-detail"),
    path("<str:username>/follow/", views.follow_toggle, name="api-follow-toggle")
]

