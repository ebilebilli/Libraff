# Generated by Django 5.1.6 on 2025-02-23 11:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comments',
            old_name='context',
            new_name='content',
        ),
    ]
