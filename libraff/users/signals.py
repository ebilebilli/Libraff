from django.db.models.signals import post_save, post_delete
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
import logging
from datetime import datetime, timezone

from users.models import CustomerUser
from .tasks import send_mail_func


@receiver(post_save, sender=CustomerUser)
def send_mail_signal(sender, instance, created, **kwargs):
    if created:
        send_mail_func.delay(instance.username, instance.email)

#log signals
logger = logging.getLogger('django')

@receiver(post_save, sender=CustomerUser)
def log_user_saved(instance, sender, created, **kwargs):
    user_id = instance.id
    if created:
        logger.info(f'User_{user_id}_created_{datetime.now(timezone.utc)}')

    else:
        logger.info(f'User_{user_id}_updated_{datetime.now(timezone.utc)}')


@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    user_id = user.id 
    logger.info(f'User_{user_id}_logged_in_{datetime.now(timezone.utc)}')


@receiver(user_logged_out)
def log_user_out(sender, request, user, **kwargs):
    user_id = user.id 
    logger.info(f'User_{user_id}_logged_in_{datetime.now(timezone.utc)}')