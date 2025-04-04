# Generated by Django 5.1.6 on 2025-03-01 15:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BookCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(blank=True, max_length=255, null=True)),
                ('title', models.CharField(blank=True, max_length=255, null=True)),
                ('context', models.CharField(blank=True, max_length=255, null=True)),
                ('price', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('like', models.IntegerField(blank=True, default=0, null=True)),
                ('pdf', models.FileField(blank=True, null=True, upload_to='books/pdf')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.bookcategory')),
            ],
        ),
    ]
