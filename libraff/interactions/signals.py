from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from interactions.models import Comment, Like
from django.core.cache import cache

@receiver([post_save, post_delete], sender=Comment)
def clean_comment_cache(instance, sender, **kwargs):
    book_id = instance.book.id
    comment_id = instance.id

    cache.delete_pattern(f'Book_{book_id}_comments_page_*')
    cache.delete(f'Comment_detail_{comment_id}')
    cache.delete_pattern(f'User_{instance.user.id}_comments_page_*')

@receiver([post_save, post_delete], sender=Like)
def clean_like_cache(instance, sender, **kwargs):
    if instance.book:
        cache.delete_pattern(f'Likes_for_book_{instance.book.id}_page_*')

    if instance.comment:
        cache.delete_pattern(f'Likes_for_comment_{instance.comment.id}_page_*')

