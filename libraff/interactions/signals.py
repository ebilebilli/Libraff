from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from interactions.models import Comment, Like
from django.core.cache import cache
import logging

#cache settings
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


#loging setting
logger = logging.getLogger('django')
@receiver(post_save, sender=Comment)
def log_comment_saved(instance, sender, created, **kwargs):
    user_id = instance.user.id
    book_id = instance.book.id
    comment_id = instance.id
    if created:
        logger.info(f'User_{user_id}_wrote_comment_{comment_id}_book_{book_id}')


@receiver(post_delete, sender=Comment)
def log_comment_deleted(instance, **kwargs):
    try:
        user_id = instance.user.id
        book_id = instance.book.id
        comment_id = instance.id
        logger.info(f'User_{user_id}_delete_comment_{comment_id}_book_{book_id}')
    except Exception as e:
        logger.warning(f'Failed to log deleted comment ID {instance.id}: {e}')

@receiver(post_save, sender=Like)
def log_like_saved(instance, sender, created, **kwargs):
    user_id = instance.user.id
    like_id = instance.id
    if instance.book:
        book_id = instance.book.id
        logger.info(f'User_{user_id}_liked_{like_id}_book_{book_id}')
    
    if instance.comment:
        comment_id = instance.comment.id
        logger.info(f'User_{user_id}_liked_{like_id}_book_{comment_id}')


@receiver(post_delete, sender=Like)
def log_comment_deleted(instance, **kwargs):
    user_id = instance.user.id
    like_id = instance.id
    try:
        if instance.book:
            book_id = instance.book.id
            logger.info(f'User_{user_id}_removed_like_{like_id}_book_{book_id}')
        
        if instance.comment:
            comment_id = instance.comment.id
            logger.info(f'User_{user_id}_removed_like_{like_id}_comment_{comment_id}')

    except Exception as e:
        logger.warning(f'Failed to log deleted like ID {instance.id}: {e}')


