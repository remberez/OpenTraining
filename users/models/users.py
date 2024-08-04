from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from .managers import CustomUserManager
from .profiles import Learner


class User(AbstractUser):
    username = models.CharField(
        verbose_name='Никнейм', max_length=25,
        unique=True, blank=True,
    )
    email = models.EmailField(
        verbose_name='Почта', unique=True, blank=True, null=True,
    )
    discord_id = models.CharField(
        verbose_name='ID дискорда', unique=True,
        max_length=25, blank=True, null=True,
    )
    is_public = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    objects = CustomUserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.username}'


@receiver(post_save, sender=User)
def post_save_user(sender, instance, created, **kwargs):
    if not hasattr(instance, 'learner_profile'):
        Learner.objects.create(
            user=instance,
            name=instance.username,
        )
