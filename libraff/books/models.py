from django.db import models

from users.models import CustomerUser

class BookCategory(models.Model):
    category_name = models.CharField(max_length=100)
    
    def __str__(self):
        return f'{self.category_name}'


class Book(models.Model):
    category = models.ForeignKey(BookCategory, on_delete=models.CASCADE)

    book_image = models.ImageField(
        upload_to='book_images/', 
        null=True,
        blank=True
    )
    author = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )
    title = models.CharField(
        max_length=255, 
        null=True, 
        blank=True
    )
    context = models.CharField(
        max_length=1000, 
        null=True, 
        blank=True
    )
    price = models.PositiveSmallIntegerField(
        null=True,
        blank=True
    )
   
    pdf = models.FileField(
        upload_to='books/pdf',
        null=True, 
        blank=True
    )

    def like_count(self):
        return f'{self.likes.count()}'

    def __str__(self):
        return f'{self.title}'


class UserBookStatus(models.Model):
    WANT_TO_READ = 'Want to Read'
    READING = 'Reading'
    FINISHED = 'Finished'
    UNREAD = 'Not Read'

    STATUS_LIST = [
        (WANT_TO_READ, 'Want to Read'),
        (READING, 'Reading'),
        (FINISHED, 'Finished'),
        (UNREAD, 'Unread')
    ]
    user = models.ForeignKey(
        CustomerUser,
        on_delete=models.CASCADE, 
        related_name='status_of_books'
    )
    book = models.ForeignKey(
        Book, 
        on_delete=models.CASCADE, 
        related_name='status_of_books'
    )
    status = models.CharField(
        max_length=25,
        default=UNREAD,
        choices=STATUS_LIST
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'book')  

    def __str__(self):
        return f'{self.user.username} - {self.book.title} - {self.status}'

    
