from django.db import models

from ckeditor.fields import RichTextField
from django.db import models
from versatileimagefield.fields import VersatileImageField
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from typing import List
from .validators import validate_phone_number


class UserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, phone_number, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(phone_number, password, **extra_fields)


class User(AbstractUser):
    username = None

    biography = models.OneToOneField(to='user.Biography',
                                     on_delete=models.CASCADE,
                                     null=True, blank=True,
                                     verbose_name=_('ბიოგრაფია'))
    phone_number = models.CharField(
        _('ტელეფონის ნომერი'),
        max_length=20,
        unique=True,
        validators=[validate_phone_number])
    email = models.EmailField(_('email address'), blank=True, unique=True)

    objects = UserManager()
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS: List[str] = []

    class Meta:
        verbose_name = _('მომხმარებელი')
        verbose_name_plural = _('მომხმარებლები')


class Post(models.Model):
    title = models.CharField(_('Title'), max_length=255)
    content = RichTextField(_('Content'))
    date = models.DateTimeField(auto_now_add=True)
    image = VersatileImageField(
        _('Image'),
        upload_to='blogpost/images/',
        blank=True,
        null=True,
    )
    user = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        verbose_name=_('User'),
    )

    def __str__(self):
        return self.title


class Likes(models.Model):
    user = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        related_name='likes',
        verbose_name=_('User'),
    )
    post = models.ForeignKey(
        'Post',
        on_delete=models.CASCADE,
        related_name='likes',
        verbose_name=_('Post'),
    )

    def __str__(self):
        return self.user.username


class Comments(models.Model):
    user = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name=_('User'),
    )
    post = models.ForeignKey(
        'Post',
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name=_('Post'),
    )
    comment = models.CharField(_('Comment'), max_length=255)

    def __str__(self):
        return self.user.username


class Follow(models.Model):
    user = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        related_name='follow',
        verbose_name=_('User'),
    )
    following = models.ManyToManyField(
        'User',
        related_name='following',
        verbose_name=_('Following'),
        blank=True,
    )

    def __str__(self):
        return self.user.username
