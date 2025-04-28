from django.db import models
from django.core.exceptions import ValidationError

from users.models import CustomerUser
from books.models import Book


class Comment(models.Model):
    user = models.ForeignKey(
        CustomerUser, 
        on_delete=models.CASCADE, 
        related_name='comments'
        )
    book = models.ForeignKey(
        Book, 
        on_delete=models.CASCADE, 
        related_name='comments'
        )
    
    content = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)

    def like_count(self):
        return f'{self.likes.count()}'

    def __str__(self):
        return f'{self.user.username}: {self.content[:50]}'


class Like(models.Model):
    user = models.ForeignKey(
        CustomerUser, 
        on_delete=models.CASCADE, 
        related_name='likes'
        )
    book = models.ForeignKey(
        Book, 
        on_delete=models.CASCADE, 
        related_name='likes', 
        null=True, 
        blank=True
        )
    comment = models.ForeignKey(
        Comment, 
        on_delete=models.CASCADE, 
        related_name='likes', 
        null=True, 
        blank=True
        )
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [
            ('user', 'book'),
            ('user', 'comment')
        ]

    def clean(self):
        if self.book and self.comment:
            raise ValidationError({'message': 'You cannot like both a book and a comment in same time'})
        if not self.book and  not self.comment:
            raise ValidationError({'message': 'You must choose at least a book or a comment'})

    def save(*args, **kwargs):
        return super().save(*args, **kwargs)
  
