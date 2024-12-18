from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Robot, Order


@receiver(post_save, sender=Robot)
def send_availability_email(sender, instance, created, **kwargs):
    if not created and instance.is_available:
        orders = Order.objects.filter(robot_serial=instance, is_robot_available=False)

        for order in orders:
            subject = f"Робот модели {instance.model} версии {instance.version} теперь в наличии"
            message = (
                f"Добрый день!\n\n"
                f"Недавно вы интересовались нашим роботом модели {instance.model}, "
                f"версии {instance.version}. Этот робот теперь в наличии.\n"
                f"Если вам подходит этот вариант - пожалуйста, свяжитесь с нами.\n\n"
                f"С уважением, ваша компания."
            )
            recipient_list = [order.customer.email]

            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                recipient_list,
                fail_silently=False
            )
            order.is_robot_available = True
            order.save()
