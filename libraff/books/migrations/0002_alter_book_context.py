# Generated by Django 5.1.6 on 2025-03-05 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='context',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
