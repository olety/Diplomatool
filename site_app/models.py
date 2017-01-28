from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone


class UserType(models.Model):
    type_name = models.CharField(max_length=255)


class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, degree, faculty, user_type, department, password=None):
        # Creates a user with a given data
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, date_of_birth, password):
        # Creates a superuser with a given data
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):

    first_name = models.CharField('first name', max_length=255, blank=True)
    last_name = models.CharField('last name', max_length=255, blank=True)
    degree = models.CharField('degree', max_length=50, blank=True)
    email = models.EmailField('email address', blank=False)
    department = models.CharField('user department', max_length=4, blank=True)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    user_type = models.ForeignKey(UserType, on_delete=models.CASCADE)

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
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='topic owner'
    )
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='topic supervisor'
    )
    level = models.CharField("level", max_length=255)
    voted_for = models.BooleanField("voted for")
    available = models.BooleanField("available")
    checked = models.BooleanField("checked")


class Faculty(models.Model):
    code = models.CharField("faculty code", max_length=4)
    name = models.CharField("faculty name", max_length=255)


class Review(models.Model):
    thesis = models.ForeignKey(
        Thesis,
        on_delete=models.CASCADE,
        verbose_name='reviewed thesis'
    )
    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,
        verbose_name='reviewed topic'
    )
    is_finished = models.BooleanField("is finished")
    finished_date = models.DateTimeField("finished date", default=timezone.now())


class Thesis(models.Model):
    supervisor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='supervisor'
    )
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='student'
    )
    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,
        verbose_name='thesis topic'
    )
    finished = models.BooleanField('finished')
    reviewed = models.BooleanField('reviewed')
    short_description = models.CharField('short description', max_length=255)


class Defense(models.Model):
    thesis = models.ForeignKey(
        Thesis,
        on_delete=models.CASCADE,
        verbose_name='defended thesis'
    )
    date = models.DateTimeField('defense date', default=timezone.now())
    successful = models.BooleanField('successful')
    second_defense = models.BooleanField('second defense required')
