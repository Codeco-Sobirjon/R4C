# Generated by Django 5.1.4 on 2024-12-18 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_alter_order_customer'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='email_sent',
            field=models.BooleanField(default=False, verbose_name='Письмо отправлено'),
        ),
        migrations.AddField(
            model_name='order',
            name='is_robot_available',
            field=models.BooleanField(default=False, verbose_name='Робот в наличии'),
        ),
    ]