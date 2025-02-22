from django.db import models
from django.contrib.auth.models import AbstractUser
from books.models import Book



class CustomerUser(AbstractUser):
    email = models.EmailField(unique=True, null=True, blank=True)
    bio = models.TextField(max_length=550, null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    def __str__(self):
        return f'{self.username}'
    

class Comments(models.Model):
    user = models.ForeignKey(CustomerUser, on_delete=models.CASCADE, related_name='comments')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='comments')
    
    content = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)

    def like_count(self):
        return f'{self.likes.count()}'

    def __str__(self):
        return f'{self.content}'


class LikeBook(models.Model):
    user = models.ForeignKey(CustomerUser, on_delete=models.CASCADE, related_name='liked_books')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'book')


class LikeComment(models.Model):
    user = models.ForeignKey(CustomerUser, on_delete=models.CASCADE, related_name='liked_comments')
    comment = models.ForeignKey(Comments, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'comment')
    
   