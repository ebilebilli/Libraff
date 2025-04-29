from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_mail_func(user_name: str, user_email: str):
     send_mail(
                f'{user_name}, your account created successfully.',
                'Welcome to Libraff',
                'ebilebilli3@gmail.com',
                [user_email],
                fail_silently=True                   
            )