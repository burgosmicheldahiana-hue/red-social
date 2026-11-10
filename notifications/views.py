from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import NotificationSerializer
from .models import Notification

# Create your views here.

class NotificationListView(generics.ListAPIView):
    serializer_class= NotificationSerializer
    permission_classes= [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(
            recipient= self.request.user
        ).select_related("sender", "post")

@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def mark_all_read(request):
    Notification.objects.filter(recipient= request.user, 
                                is_read= False).update(is_read=True)
    return Response({"detail": "Notificaciones marcadas como leídas"})

