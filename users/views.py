from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer, UserMinimalSerializer, UserProfileSerializer


# Create your views here.

User= get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset= User.objects.all() 
    serializer_class= RegisterSerializer
    permission_classes= [permissions.AllowAny] 

class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class= UserProfileSerializer
    permission_classes= [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user 

class UserDetailView(generics.RetrieveAPIView):
    queryset= User.objects.all() 
    serializer_class= UserProfileSerializer
    permission_classes= [permissions.IsAuthenticated]
    lookup_field= "username"


class UserListView(generics.ListAPIView):
    serializer_class= UserMinimalSerializer
    permission_classes= [permissions.IsAuthenticated] 

    def get_queryset(self):
        qs= User.objects.exclude(pk=self.request.user.pk)
        query= self.request.query_params.get("q", "")
        if query:
            qs= qs.filter(username__icontains=query)
        return qs.order_by("first_name") 


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def follow_toggle(request, username):
    try: 
        target= User.objects.get(username= username)
    except User.DoesNotExist:
        return Response ({"detail": "Usuario no encontrado"}, status=404)

    if target == request.user:
        return Response ({"detail": "No puedes seguirte a ti mismo"}, status=400)

    if request.user.following.filter(pk=target.pk).exists():
        request.user.following.remove(target)

        following= False
    else:
        request.user.following.add(target)
        following= True

    return Response({"following": following, "followers_count": target.followers_count})










