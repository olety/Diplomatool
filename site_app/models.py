from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, Group
from django.core.mail import send_mail
from django.utils import timezone
from django.db import models
from model_utils import Choices
from datetime import timedelta

LEVELS = Choices('Bachelor', 'Master', 'Doctor')


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
    """
    User class represents the User table in the database. It implements functionalities required by Django and contains
    following attributes:
    index_number, first_name, last_name, degree, email, department, faculty, is_admin
    which can be used to access database regardless of the language it uses
    Methods:
    is_staff(), has_proposed_topic(), __str__(), is_superuser(), is_reviewer(), is_student()
    """
    index_number = models.CharField('index number', max_length=10, default='000001')
    first_name = models.CharField('first name', max_length=255,
                                  null=True, blank=True, default='Name')
    last_name = models.CharField('last name', max_length=255,
                                 null=True, blank=True, default='Surname')
    degree = models.CharField('degree', max_length=50, null=True, blank=True, choices=LEVELS, default=LEVELS.Bachelor)
    email = models.EmailField('email address', blank=False, unique=True)
    department = models.CharField('user department', max_length=4, null=True, blank=True)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, null=True,
                                blank=True, verbose_name='user faculty')
    # password is inherited
    is_admin = models.BooleanField('is admin', default=False)

    @property
    def is_staff(self):
        """
        Checks whether user is a staff member (function required by Django for User class)

        :return: Indicator whether user is a staff member
        :rtype: bool
        """
        return self.is_admin

    @property
    def has_proposed_topic(self):
        """
        Checks whether user has proposed a topic

        :return: Indicator whether user has submitted a topic
        :rtype: bool
        """
        return True if Topic.objects.filter(student_id=self.id) else False

    @property
    def is_superuser(self):
        """
        Checks whether user is a superuser

        :return: Indicator whether user is an admin
        :rtype: bool
        """
        return self.is_admin

    @property
    def is_reviewer(self):
        """
        Checks whether user is a reviewers

        :return: Indicator whether user is a reviewer
        :rtype: bool
        """
        return self.is_staff or self.groups.filter(name='Reviewer')

    @property
    def is_student(self):
        """
        Checks whether user is a student

        :return: Indicator whether user is a student
        :rtype: bool
        """
        return self.is_staff or self.groups.filter(name='Student')

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
    student = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='topic owner',
                                related_name='topic_owner', null=True, blank=True)
    supervisor = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='topic supervisor',
                                   related_name='topic_supervisor', null=True, blank=True)
    name = models.CharField('topic', max_length=255)
    level = models.CharField('level', max_length=255, null=True, blank=True, choices=LEVELS, default=LEVELS.Bachelor)
    voted_for = models.NullBooleanField('voted for', null=True, blank=True, default=False)
    available = models.NullBooleanField('available', null=True, blank=True, default=False)
    checked = models.NullBooleanField('checked', null=True, blank=True, default=False)
    short_description = models.CharField('short description', max_length=255, null=True, blank=True)
    REQUIRED_FIELDS = ['name', ]

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        full_name = 'Topic: {}'.format(self.name)
        return full_name.strip()

    def get_short_name(self):
        return self.name


class Thesis(models.Model):
    """
    Thesis class represents the Thesis table in the database. It contains following attributes:
    supervisor, student, topic, finished, finished_date, file
    which can be used to access database regardless of the language it uses
    Methods:
    get_file_path(filename), reviewed(), __str__(), get_thesis_name()
    """

    class Meta:
        """
        Meta class required by administration tools of Django
        """
        app_label = 'site_app'
        verbose_name = 'thesis'
        verbose_name_plural = 'theses'
        abstract = False

    supervisor = models.ForeignKey(User, on_delete=models.CASCADE,
                                   verbose_name='supervisor', related_name='supervisor')
    student = models.ForeignKey(User, on_delete=models.CASCADE,
                                verbose_name='student', related_name='student')
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE,
                              verbose_name='thesis topic', related_name='thesis_topic')
    finished = models.BooleanField('finished')
    finished_date = models.DateTimeField('finished date', default=timezone.now)

    def get_file_path(self, filename):
        """
        Function used to retrieve the file path for specific thesis file.

        :param filename: (string) Name of the thesis file
        :return: The full path of the requested thesis file
        :rtype: string
        """
        # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
        return 'theses/student_{0}/{1}'.format(self.student.id, filename)

    file = models.FileField(upload_to=get_file_path, verbose_name='thesis file', null=True, blank=True)

    @property
    def reviewed(self):
        """
        Checks whether thesis was reviewed

        :return: Indicator if the thesis was reviewed
        :rtype: bool
        """
        return Review.objects.filter(thesis__id=self.id).exists()

    def __str__(self):
        """
        Used to get the string representation of Thesis model. Overrides default __str__() function.

        :return: String representation of Thesis
        :rtype: string
        """
        return self.get_thesis_name

    @property
    def get_thesis_name(self):
        """
        Gets a formatted review name for string representation of Thesis.

        :return: Thesis name and author
        :rtype: string
        """
        thesis_name = '{} by {}'.format(self.topic.name, self.student.get_full_name())
        return thesis_name.strip()


class Review(models.Model):
    """
    Review class represents the Review table in the database. It contains following attributes:
    author, thesis, finished, finished_date
    which can be used to access database regardless of the language it uses
    Methods:
    deadline(), get_file_path(filename), __str__(), get_review_name()
    """
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               verbose_name='review author', related_name='review_author')
    thesis = models.ForeignKey(Thesis, on_delete=models.CASCADE,
                               verbose_name='reviewed thesis', related_name='reviewed_thesis')

    # We can reference a topic via thesis
    @property
    def finished(self):
        """
        Used to see whether the review was finished or not.
        :return: Indicator if the review was finished
        :rtype: bool
        """
        return True if self.file.name else False

    finished_date = models.DateTimeField('finished date', null=True, blank=True, default=None)

    @property
    def deadline(self):
        """
        Used to calculate the deadline of current review.

        :return: The date by which review has to be submitted
        :rtype: datetime
        """
        return self.thesis.finished_date.date() + timedelta(weeks=2)

    def get_file_path(self, filename):
        """
        Function used to retrieve the file path for specific review file.

        :param filename: (string) Name of the review file
        :return: The full path of the requested review file
        :rtype: string
        """
        file_ext = filename.split('.')[-1]
        return 'theses/thesis_{0}/review.{1}'.format(self.thesis.id, file_ext)

    file = models.FileField(upload_to=get_file_path, verbose_name='review file', null=True, blank=True)

    def __str__(self):
        """
        Used to get the string representation of Review model. Overrides default __str__() function.

        :return: String representation of Review
        :rtype: string
        """
        return self.get_review_name

    def get_review_name(self):
        """
        Gets a formatted review name for string representation of Review.

        :return: Review ID, author and the name of thesis under review
        :rtype: string
        """
        review_name = 'Review #{} by {} of {}'.format(self.id, self.author, self.thesis.get_thesis_name)
        return review_name.strip()


class Defense(models.Model):
    """
    Defense class represents the Defense table in the database. It contains following attributes:
    thesis, date, successful, second_defense
    which can be used to access database regardless of the language it uses
    Methods:
    __str__, get_defense_name()
    """
    thesis = models.ForeignKey(Thesis, on_delete=models.CASCADE,
                               verbose_name='defended thesis', related_name='defended_thesis')
    date = models.DateTimeField('defense date', default=timezone.now)
    successful = models.BooleanField('successful')
    second_defense = models.BooleanField('second defense required')

    def __str__(self):
        """
        Used to get the string representation of a Defense model. Overrides default __str__() function.

        :return: String representation of Defense
        :rtype: string
        """
        return self.get_defense_name

    def get_defense_name(self):
        """
        Gets a formatted review name for string representation of Defense.

        :return: Defense ID and name of defended thesis
        :rtype: string
        """
        defense_name = 'Defense #{} of {}'.format(self.id, self.thesis.get_thesis_name)
        return defense_name.strip()
