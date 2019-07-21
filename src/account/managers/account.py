from django.conf import settings
from django.contrib.auth import password_validation
from django.contrib.auth.base_user import BaseUserManager
from django.utils.crypto import get_random_string


class UserManager(BaseUserManager):
    """
    Продублировал дефолтный UserManager с заменой "username" на "email"
    (без этого create_user падал с ошибкой)
    """
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given login, email, and password.
        """
        if not email:
            raise ValueError('The given login must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

    def generate_password(self):
        while True:
            password = get_random_string(length=settings.PASSWORD_MAX_LENGTH)

            try:
                password_validation.validate_password(password=password)
            except Exception:
                pass
            else:
                break
        return password
