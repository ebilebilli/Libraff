from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomerUser(AbstractUser):
    email = models.EmailField(
        unique=True, 
        null=True, 
        blank=True
    )
    bio = models.TextField(
        max_length=550, 
        null=True, 
        blank=True
    )
    avatar = models.ImageField(
        upload_to='avatars/', 
        null=True, 
        blank=True
    )

    def __str__(self):
        return f'{self.username}'
    


    
   