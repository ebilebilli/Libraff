# Generated by Django 5.1.7 on 2025-03-07 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0003_book_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='book_image',
            field=models.ImageField(blank=True, null=True, upload_to='book_images/'),
        ),
    ]
