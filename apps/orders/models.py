from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth import get_user_model
from django.db import models
from django.core.mail import send_mail
from django.conf import settings
from apps.orders.manager import RobotManager
from apps.robots.models import Robot


class Order(models.Model):
    customer = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True, blank=True, verbose_name="Клиент")
    robot_serial = models.ForeignKey(Robot, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Робот')
    quantity = models.IntegerField(default=0, null=True, blank=True, verbose_name='Количество')
    created = models.DateTimeField(blank=False, null=False, auto_now_add=True, verbose_name='Дата создания')
    is_robot_available = models.BooleanField(default=False, verbose_name="Робот в наличии")
    email_sent = models.BooleanField(default=False, verbose_name="Письмо отправлено")

    objects = RobotManager()

    def __str__(self):
        return f"Order {self.id}"

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['created']

