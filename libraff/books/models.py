from django.db import models

# Create your models here.



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

    def __str__(self):
        return f'{self.title}'
