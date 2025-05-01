from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from favorites.models import Favorite
from django.core.cache import cache

@receiver([post_save, post_delete], sender=Favorite)
def clean_favorite_cache(instance, sender, **kwargs):
    user_id = instance.user.id
    favorite_id = instance.id

    cache.delete_pattern(f'User_{user_id}_open_favorites_*')
    cache.delete_pattern(f'User_{user_id}_private_favorites_*')
    cache.delete(f'Favorite_detail_{favorite_id}')
 