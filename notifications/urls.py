from django.urls import path
from . import views

urlpatterns = [
    path("", views.NotificationListView.as_view(), name="api-notifications"),
    path("read-all/", views.mark_all_read, name="api-notifications-read"),
]