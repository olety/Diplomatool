from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone

# Create your models here.


class UserType(models.Model):
    type_name = models.CharField(max_length=255)


class UserManager(BaseUserManager):
    def create_user(self, email, name, surname, degree, faculty, user_type, password=None):
        """
        Creates and saves a User with the given email data
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            date_of_birth=date_of_birth,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, date_of_birth, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            date_of_birth=date_of_birth,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):

    first_name = models.CharField('first name', max_length=30, blank=True)
    last_name = models.CharField('last name', max_length=30, blank=True)
    email = models.EmailField('email address', blank=True)

    date_joined = models.DateTimeField('date joined', default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        abstract = True

    def get_full_name(self):
        full_name = '{} {}'.format(self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)


class Topic(models.Model):
    level = models.CharField(max_length=255)
    voted_for = models.BooleanField()
    available = models.BooleanField()
    checked = models.BooleanField()


class Faculty(models.Model):
    code = models.CharField(max_length=4)
    name = models.CharField(max_length=255)


class Review(models.Model):
    is_finished = models.BooleanField()
    finished_date = models.DateTimeField(default=timezone.now())


class Thesis(models.Model):
    finished = models.BooleanField()
    reviewed = models.BooleanField()
    short_description = models.CharField(max_length=255)


class Defense(models.Model):
    date = models.DateTimeField(default=timezone.now())
    successful = models.BooleanField()
    second_defense = models.BooleanField()
