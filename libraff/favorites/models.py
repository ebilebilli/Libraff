from django.db import models

from books.models import Book
from users.models import CustomerUser


class Favorite(models.Model):
    PRIVATE = 'Private'
    OPEN = 'Open'

    STATUS_LIST = [
        (PRIVATE, 'Private'),
        (OPEN, 'Open')
    ]

    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='favorites'
    )
    user = models.ForeignKey(
        CustomerUser, 
        on_delete=models.CASCADE, 
        related_name='favorites'
    )

    status = models.CharField(
        choices=STATUS_LIST,
        default=OPEN
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [
            ('user', 'book'),
        ]

    def __str__(self):
        return f'{self.user.username} favorited {self.book.title} '
