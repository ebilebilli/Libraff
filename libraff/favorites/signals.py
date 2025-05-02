from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
import logging

from favorites.models import Favorite


#cache signals
@receiver([post_save, post_delete], sender=Favorite)
def clean_favorite_cache(instance, sender, **kwargs):
    user_id = instance.user.id
    favorite_id = instance.id

    cache.delete_pattern(f'User_{user_id}_open_favorites_*')
    cache.delete_pattern(f'User_{user_id}_private_favorites_*')
    cache.delete(f'Favorite_detail_{favorite_id}')
 

#log signals
logger = logging.getLogger('django')

@receiver(post_save, sender=Favorite)
def log_favorite_saved(instance, sender, created, **kwargs):
    user_id = instance.user.id
    favorite_id = instance.id
    book_id = instance.book.id
    if created:
        logger.info(f'User_{user_id}_add_favorite_{favorite_id}_book_{book_id}')

    else:
        logger.info(f'User_{user_id}__favorite_{favorite_id}_book_{book_id}')
        

@receiver(post_delete, sender=Favorite)
def log_favorite_deleted(instance, **kwargs):
    user_id = instance.user.id
    favorite_id = instance.id
    book_id = instance.book.id
    try:
        logger.info(f'User_{user_id}_removed_favorite_{favorite_id}_book_{book_id}')
    
    except Exception as e:
        logger.warning(f'Failed to log deleted favorite ID {instance.id}: {e}')
