import pdb

from django.contrib.auth.base_user import BaseUserManager
from rest_framework.exceptions import ParseError


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(
            self, email=None, discord_id=None, username=None, password=None, **extra_fields
    ):
        if not (email or username or discord_id):
            raise ParseError('Укажите дискорд или номер телефона')

        if not username:
            if email:
                email = self.normalize_email(email)
                username = email.split('@')[0]
            else:
                username = discord_id

        user = self.model(username=username, **extra_fields)
        if email:
            user.email = email

        if discord_id:
            user.discord_id = discord_id

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
            self, email=None, username=None, discord_id=None, password=None, **extra_fields
    ):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        return self._create_user(email, discord_id, username, password, **extra_fields)

    def create_user(
            self, email=None, username=None, discord_id=None, password=None, **extra_fields
    ):
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_active', True)
        return self._create_user(email, discord_id, username, password, **extra_fields)
