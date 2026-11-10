from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from posts.models import Like, Comment
from .models import Notification
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(post_save, sender=Like)
def notify_like(sender, instance, created, **kwargs):
    if created and instance.user != instance.post.author:
        Notification.objects.create(
            recipient= instance.post.author,
            sender= instance.user,
            notification_type= "like",
            post= instance.post,
        )

@receiver(post_save, sender=Comment)
def notify_comment(sender, instance, created, **kwargs):
    if created and instance.author != instance.post.author:
        Notification.objects.create(
            recipient= instance.post.author,
            sender= instance.author,
            notification_type= "comment",
            post= instance.post,
        )

@receiver(m2m_changed, sender=User.following.through)
def notify_follow(sender, instance, action, pk_set, **kwargs):
    if action == "post_add":
        for user_id in pk_set:
            try:
                followed_user = User.objects.get(pk=user_id)
                if instance != followed_user:
                    Notification.objects.create(
                        recipient= followed_user,
                        sender= instance,
                        notification_type= "follow",
                    )
            except User.DoesNotExist:
                continue