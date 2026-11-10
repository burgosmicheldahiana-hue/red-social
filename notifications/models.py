from django.db import models
from django.conf import settings
# Create your models here.

class Notification(models.Model):
    TYPES= [
        ("like", "Like en tu post"),
        ("comment", "Comentario en tu post"),
        ("follow", "Alguien te siguió")
    ]

    recipient= models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete= models.CASCADE,
        related_name="notifications",
    )

    sender= models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete= models.CASCADE,
        related_name="sent_notifications",
    )

    notification_type= models.CharField(max_length=30, choices=TYPES) 

    post = models.ForeignKey(
        "posts.Post",
        on_delete= models.CASCADE,
        null= True,
        blank= True, 
    )

    is_read= models.BooleanField(default=False)
    created_at= models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering= ["-created_at"] 





