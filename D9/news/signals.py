from django.db.models.signals import post_save
from django.dispatch import receiver  # импортируем нужный декоратор
from django.core.mail import mail_managers
from .models import Post


# в декоратор передаётся первым аргументом сигнал, на который будет реагировать эта функция, и в отправители надо передать также модель
@receiver(post_save, sender=Post)
def notify_subscriber(sender, instance, created, **kwargs):
    if created:
        print(type(instance))
        #subject = f'{instance.username} {instance.head}'

        #subject = f'{instance.username} {instance.created.strftime("%d %m %Y")}'
    # else:
    #     subject = f'Appointment changed for {instance.client_name} {instance.date.strftime("%d %m %Y")}'

    # mail_managers(
    #     subject=subject,
    #     message=instance.text,
    # )