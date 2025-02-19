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
    like = models.IntegerField(default=0)
    pdf = models.FileField(upload_to='books/pdf')

    def __str__(self):
        return f'{self.title}'
    
