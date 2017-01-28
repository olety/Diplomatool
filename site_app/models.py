from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.mail import send_mail
from django.utils import timezone
from django.db import models


class UserType(models.Model):
    type_name = models.CharField(max_length=255)

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        full_name = 'Type: {}'.format(self.type_name)
        return full_name.strip()

    def get_short_name(self):
        return self.type_name


class Faculty(models.Model):
    class Meta:
        app_label = 'site_app'
        verbose_name = 'faculty'
        verbose_name_plural = 'faculties'
        abstract = False

    code = models.CharField('faculty code', max_length=4)
    name = models.CharField('faculty name', max_length=255)

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        full_name = '{}: {}'.format(self.code, self.name)
        return full_name.strip()

    def get_short_name(self):
        return self.name


class UserManager(BaseUserManager):
    def create_user(self, email, **kwargs):
        # Creates a user with a given data
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            **kwargs
        )

        user.set_password(kwargs.get('password', ''))
        user.save()
        return user

    def create_superuser(self, email, password, **kwargs):
        # Creates a superuser with a given data
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            **kwargs
        )
        user.is_admin = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):

    first_name = models.CharField('first name', max_length=255, null=True, blank=True, default='Name')
    last_name = models.CharField('last name', max_length=255, null=True, blank=True, default='Surname')
    degree = models.CharField('degree', max_length=50, null=True, blank=True, default='Degree')
    email = models.EmailField('email address', blank=False, unique=True)
    department = models.CharField('user department', max_length=4, null=True, blank=True)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, null=True, blank=True, verbose_name='user faculty')
    type = models.ForeignKey(UserType,
                             on_delete=models.CASCADE,
                             null=True,
                             blank=True,
                             default='Student',
                             verbose_name='user type')
    # password is inherited
    is_admin = models.BooleanField('is admin', default=False)

    @property
    def is_staff(self):
        return self.is_admin

    @property
    def is_superuser(self):
        return self.is_admin

    objects = UserManager()

    USERNAME_FIELD = 'email'

    class Meta:
        app_label = 'site_app'
        verbose_name = 'user'
        verbose_name_plural = 'users'
        abstract = False

    def __str__(self):
        return '{}: {}'.format(self.email, self.get_full_name())

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
        verbose_name='topic owner',
        related_name='topic_owner',
        null=True,
        blank=True
    )

    supervisor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='topic supervisor',
        related_name='topic_supervisor',
        null=True,
        blank=True
    )

    name = models.CharField('topic', max_length=255)
    level = models.CharField('level', max_length=255, null=True, blank=True, default='Bachelor')
    voted_for = models.NullBooleanField('voted for', null=True, blank=True)
    available = models.NullBooleanField('available', null=True, blank=True)
    checked = models.NullBooleanField('checked', null=True, blank=True)
    REQUIRED_FIELDS = ['name', ]

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        full_name = 'Topic: {}'.format(self.name)
        return full_name.strip()

    def get_short_name(self):
        return self.name


class Thesis(models.Model):
    supervisor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='supervisor',
        related_name='supervisor'
    )
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='student',
        related_name='student'
    )
    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,
        verbose_name='thesis topic',
        related_name='thesis_topic'
    )
    finished = models.BooleanField('finished')
    reviewed = models.BooleanField('reviewed')
    short_description = models.CharField('short description', max_length=255)

    def __str__(self):
        return self.get_thesis_name()

    def get_thesis_name(self):
        thesis_name = 'Thesis: {} {}'.format(self.topic.name, self.student.get_full_name())
        return thesis_name.strip()


class Review(models.Model):
    thesis = models.ForeignKey(
        Thesis,
        on_delete=models.CASCADE,
        verbose_name='reviewed thesis',
        related_name='reviewed_thesis'
    )
    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,
        verbose_name='reviewed topic',
        related_name='reviewed_topic'
    )
    is_finished = models.BooleanField('is finished')
    finished_date = models.DateTimeField('finished date', default=timezone.now)

    def __str__(self):
        return self.get_review_name()

    def get_review_name(self):
        review_name = 'Review: {} {}'.format(self.id, self.thesis.get_thesis_name())
        return review_name.strip()


class Defense(models.Model):
    thesis = models.ForeignKey(
        Thesis,
        on_delete=models.CASCADE,
        verbose_name='defended thesis',
        related_name='defended_thesis'
    )
    date = models.DateTimeField('defense date', default=timezone.now)
    successful = models.BooleanField('successful')
    second_defense = models.BooleanField('second defense required')

    def __str__(self):
        return self.get_defense_name()

    def get_defense_name(self):
        defense_name = 'Defense: {} {}'.format(self.id, self.thesis.get_thesis_name())
        return defense_name.strip()
