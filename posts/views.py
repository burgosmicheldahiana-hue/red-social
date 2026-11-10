from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from .models import Post, Like, Comment
from .serializers import PostSerializer, CommentSerializer

# Create your views here.

class FeedView(generics.ListAPIView):
    serializer_class= PostSerializer
    permission_classes= [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        following_ids= list(user.following.values_list("id", flat=True))

        return (
            Post.objects.filter(author_id__in= following_ids)
            .select_related("author")
            .prefetch_related("likes", "comments")
        )

class PostListCreateView(generics.ListCreateAPIView):
    serializer_class= PostSerializer
    permission_classes= [permissions.IsAuthenticated] 

    def get_queryset(self):
        qs = Post.objects.select_related("author").prefetch_related("likes", "comments")
        author = self.request.query_params.get("author")
        if author:
            qs = qs.filter(author__username=author)
        return qs

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class= PostSerializer
    permission_classes= [permissions.IsAuthenticated] 
    def get_queryset(self):
        return Post.objects.select_related("author")

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied("No puedes editar este post")

        serializer.save()

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied("No puedes eliminar este post")
        instance.delete()


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def like_toggle(request, pk):
    try:
        post= Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response ({"detail": "Post no encontrado"}, status=404)

    like, created= Like.objects.get_or_create(user= request.user, post=post)
    if not created:
        like.delete()
        liked = False
    else: 
        liked= True

    return Response({"liked": liked, "likes_count":post.likes_count})


class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class= CommentSerializer
    permission_classes= [permissions.IsAuthenticated] 
    def get_queryset(self):
        return (Comment.objects.filter(post_id= self.kwargs["pk"])
                .select_related("author")) 

    def perform_create(self, serializer):
        post= get_object_or_404(Post, pk=self.kwargs["pk"])
        serializer.save(author= self.request.user, post=post)



