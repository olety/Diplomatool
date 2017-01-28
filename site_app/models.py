from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone


class UserType(models.Model):
    type_name = models.CharField(max_length=255)


class Faculty(models.Model):
    code = models.CharField("faculty code", max_length=4)
    name = models.CharField("faculty name", max_length=255)


class UserManager(BaseUserManager):
    def create_user(self, email, first_name=None, last_name=None, degree=None, faculty=None, type=None, department=None, password=None):
        # Creates a user with a given data
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            degree=degree,
            faculty=faculty,
            type=type,
            department=department
        )

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, first_name=None, last_name=None, degree=None, faculty=None, type=None, department=None):
        # Creates a superuser with a given data
        user = self.create_user(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            degree=degree,
            faculty=faculty,
            type=type,
            department=department,
            password=password
        )
        user.is_admin = True
        user.save()
        return user


class User(AbstractBaseUser):

    first_name = models.CharField('first name', max_length=255, null=True)
    last_name = models.CharField('last name', max_length=255, null=True)
    degree = models.CharField('degree', max_length=50, null=True)
    email = models.EmailField('email address', blank=False, unique=True)
    department = models.CharField('user department', max_length=4, null=True)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, null=True, verbose_name='user faculty')
    type = models.ForeignKey(UserType, on_delete=models.CASCADE, null=True, verbose_name='user type')
    # password is inherited
    is_admin = models.BooleanField('is admin', default=False)
    objects = UserManager()

    USERNAME_FIELD = 'email'

    class Meta:
        app_label = 'site_app'
        verbose_name = 'user'
        verbose_name_plural = 'users'
        abstract = False

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
        related_name='topic_owner'
    )
    supervisor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='topic supervisor',
        related_name='topic_supervisor'
    )
    level = models.CharField("level", max_length=255)
    voted_for = models.BooleanField("voted for")
    available = models.BooleanField("available")
    checked = models.BooleanField("checked")


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
    is_finished = models.BooleanField("is finished")
    finished_date = models.DateTimeField("finished date", default=timezone.now)


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