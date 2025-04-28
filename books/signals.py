from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache

from books.models import BookCategory, Book


#BookCategory, Book, cache settings
@receiver([post_save, post_delete], sender=BookCategory)
def clean_book_category_cache(instance, sender, **kwargs):
    cache.delete_pattern('Book_category_list')

@receiver([post_save, post_delete], sender=Book)
def clean_book_cache(instance, sender, **kwargs):
    cache.delete_pattern('Book_list')

@receiver([post_save, post_delete], sender=Book)
def clean_book_for_category_cache(instance, sender, **kwargs):
    cache.delete_pattern(f'Book_list_for_category_{instance.category.id}_*')

@receiver([post_save, post_delete], sender=Book)
def clean_book_detail_cache(instance, sender, **kwargs):
    cache.delete_pattern(f'Book_detail_{instance.id}_*')

