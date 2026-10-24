from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin


class UserManager(BaseUserManager):
    def _user(self, email: str, password: str | None = None, admin: bool = False, **kwargs):
        if not email:
            raise ValueError('User must have an email address')
        user = self.model(email=self.normalize_email(email), is_superuser=admin, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email: str, password: str | None = None, **kwargs):
        kwargs['admin'] = False
        return self._user(email, password, **kwargs)

    def create_superuser(self, email: str, password: str | None = None, **kwargs):
        kwargs['admin'] = True
        return self._user(email, password, **kwargs)


class User(AbstractBaseUser, PermissionsMixin):
    id = models.BigAutoField(primary_key=True)

    email = models.EmailField(max_length=255, unique=True)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    objects = UserManager()

    def __str__(self):
        return getattr(self, self.USERNAME_FIELD)

    class Meta:
        db_table = 'users'
