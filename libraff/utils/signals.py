from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models import CustomerUser
from .tasks import send_mail_func

@receiver(post_save, sender=CustomerUser)
def send_mail_signal(sender, instance, created, **kwargs):
    if created:
        send_mail_func(instance.username, instance.email)

