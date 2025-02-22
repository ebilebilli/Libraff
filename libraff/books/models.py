from django.db import models


class Book(models.Model):
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
    price = models.PositiveSmallIntegerField(
        null=True,
        blank=True
    )
    like = models.IntegerField(
        default=0, 
        null=True,
        blank=True
    )
    pdf = models.FileField(
        upload_to='books/pdf',
        null=True, 
        blank=True
    )

    def __str__(self):
        return f'{self.title}'


