from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import TemplateView
from django.views.static import serve

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("healthz/", views.health, name="health"),
    path("admin/", admin.site.urls),
    # Páginas (templates)
    path("login/", TemplateView.as_view(template_name="login.html"), name="login"),
    path("register/", TemplateView.as_view(template_name="register.html"), name="register"),
    path("feed/", TemplateView.as_view(template_name="feed.html"), name="feed"),
    path("profile/", TemplateView.as_view(template_name="profile.html"), name="profile"),
    path("notifications/", TemplateView.as_view(template_name="notifications.html"), name="notifications"),
    # API
    path("api/users/", include("users.urls")),
    path("api/posts/", include("posts.urls")),
    path("api/notifications/", include("notifications.urls")),
    # Media (disco local; en Render es efímero salvo que montes un Disk)
    re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
]
