from django.db import models
from django.contrib.auth.models import AbstractUser 


# Create your models here.

class User(AbstractUser):

    email= models.EmailField(unique=True)
    bio= models.TextField(max_length=300, blank=True)
    department= models.CharField(max_length=100, blank=True)
    position= models.CharField(max_length=100, blank=True)

    following = models.ManyToManyField(
        "self",
        symmetrical=False, 
        related_name="followers",
        blank=True,
    )

    USERNAME_FIELD = "email" 
    REQUIRED_FIELDS= ["username", "first_name", "last_name"] 

    @property
    def followers_count(self):
        return self.followers.count()

    @property
    def following_count(self):
        return self.following.count() 

