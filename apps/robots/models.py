from django.db import models


class Robot(models.Model):
    serial = models.CharField(max_length=5, blank=False, null=False, unique=True, verbose_name="Серийный номер")
    model = models.CharField(max_length=2, blank=False, null=False, verbose_name="Модель")
    version = models.CharField(max_length=2, blank=False, null=False, verbose_name="Версия")
    is_available = models.BooleanField(default=False, verbose_name="В наличии")
    created = models.DateTimeField(blank=False, null=False, auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return f"{self.model} - {self.serial}"

    class Meta:
        verbose_name = 'Робот'
        verbose_name_plural = 'Роботы'
        ordering = ['created']