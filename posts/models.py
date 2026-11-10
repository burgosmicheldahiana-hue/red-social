from django.db import models
from django.conf import settings

# Create your models here.
class Post(models.Model):
    author= models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="posts", 
    )
    content= models.TextField(max_length=1000)
    image= models.ImageField(upload_to="posts/", blank=True)
    created_at= models.DateTimeField(auto_now_add=True) 
    updated_at= models.DateTimeField(auto_now=True) 

    @property
    def likes_count(self):
        return self.likes.count()

    @property
    def comments_count(self):
        return self.comments.count()


class Like(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="likes",        
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="likes" 
    )
    created_at=models.DateTimeField(auto_now_add=True) 

    class Meta: 
        unique_together= ("user", "post") 


class Comment(models.Model):
    author= models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comments", 
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments" 
    )   
    content= models.TextField(max_length=1000)
    created_at= models.DateTimeField(auto_now_add=True) 

    class Meta: 
        ordering= ["created_at"] 
