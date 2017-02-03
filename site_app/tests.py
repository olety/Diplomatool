import os
from django.conf import settings
from django.test import TestCase, Client
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from django.utils import timezone
import shutil
import ntpath
from . import models


# Unit tests


class StudentTestCase(TestCase):
    mock_email = 'student@test.test'
    mock_password = 'testpass123'

    def setUp(self):
        g = models.Group.objects.create(name='Student')
        stud = models.User.objects.create_user(email=self.mock_email, password=self.mock_password)
        g.user_set.add(stud)

        self.client = Client()

    def test_student_created(self):
        self.assertTrue(models.User.objects.filter(email=self.mock_email).exists())

    def test_student_in_group(self):
        try:
            student = models.User.objects.filter(email=self.mock_email)[0]
        except IndexError:
            self.fail()
        self.assertTrue(student.groups.all().filter(name='Student').exists())

    def test_student_can_view_profile(self):
        self.client.login(username=self.mock_email, password=self.mock_password)
        self.assertEqual(self.client.get(reverse('profile')).status_code, 200)

    def test_student_can_view_topics(self):
        self.client.login(username=self.mock_email, password=self.mock_password)
        self.assertEqual(self.client.get(reverse('topic_list')).status_code, 200)

    def test_student_can_not_view_reviews(self):
        self.client.login(username=self.mock_email, password=self.mock_password)
        self.assertEqual(self.client.get(reverse('reviews')).status_code, 302)


class ReviewerTestCase(TestCase):
    mock_email = 'reviewer@test.test'
    mock_password = 'testpass123'

    def setUp(self):
        g = models.Group.objects.create(name='Reviewer')
        stud = models.User.objects.create_user(email=self.mock_email, password=self.mock_password)
        g.user_set.add(stud)
        self.client = Client()

    def test_student_created(self):
        self.assertTrue(models.User.objects.filter(email=self.mock_email).exists())

    def test_reviewer_in_group(self):
        try:
            reviewer = models.User.objects.filter(email=self.mock_email)[0]
        except IndexError:
            self.fail()
        self.assertTrue(reviewer.groups.all().filter(name='Reviewer').exists())

    def test_student_can_view_profile(self):
        self.client.login(username=self.mock_email, password=self.mock_password)
        self.assertEqual(self.client.get(reverse('profile')).status_code, 200)

    def test_student_can_view_topics(self):
        self.client.login(username=self.mock_email, password=self.mock_password)
        self.assertEqual(self.client.get(reverse('topic_list')).status_code, 302)

    def test_student_can_not_view_reviews(self):
        self.client.login(username=self.mock_email, password=self.mock_password)
        self.assertEqual(self.client.get(reverse('reviews')).status_code, 200)


# Integration

class StudentTopicTestCase(TestCase):
    mock_data = {
        'stud_email': 'student@test.test',
        'stud_password': 'testpass123',
        'super_email': 'supervisor@test.test',
        'super_password': 'testpass123',
        'topic_name': 'Topic test name',
        'topic_desc': 'Short description'
    }

    def setUp(self):
        supervisors = models.Group.objects.create(name='Supervisor')
        students = models.Group.objects.create(name='Student')
        self.stud = models.User.objects.create_user(email=self.mock_data['stud_email'],
                                                    password=self.mock_data['stud_password'])
        self.supervisor = models.User.objects.create_user(email=self.mock_data['super_email'],
                                                          password=self.mock_data['super_password'])
        supervisors.user_set.add(self.supervisor)
        students.user_set.add(self.stud)
        self.client = Client()

    def test_student_can_propose_topic(self):
        self.client.login(username=self.stud.email, password=self.mock_data['stud_password'])
        self.client.post(reverse('topic_list'), {
            'name': self.mock_data['topic_name'],
            'description': self.mock_data['topic_desc'],
            'supervisor': self.supervisor.id
        })
        try:
            proposed_topic = models.Topic.objects.filter(student__id=self.stud.id)[0]
        except IndexError:
            self.fail('Topic was not created')
        self.assertTrue(proposed_topic is not None)
        self.assertEqual(proposed_topic.name, self.mock_data['topic_name'])
        self.assertEqual(proposed_topic.short_description, self.mock_data['topic_desc'])
        self.assertEqual(proposed_topic.supervisor, self.supervisor)
        self.assertEqual(proposed_topic.student, self.stud)


class SendReviewTestCase(TestCase):
    mock_data = {
        'rev_email': 'reviewer@test.test',
        'rev_password': 'testpass123',
        'stud_email': 'student@test.test',
        'stud_password': 'testpass123',
        'super_email': 'supervisor@test.test',
        'super_password': 'testpass123',
        'topic_name': 'Topic test name',
        'topic_desc': 'Short description'
    }

    def setUp(self):
        # Creating user groups
        supervisors = models.Group.objects.create(name='Supervisor')
        students = models.Group.objects.create(name='Student')
        reviewers = models.Group.objects.create(name='Reviewer')
        # Creating users
        self.stud = models.User.objects.create_user(email=self.mock_data['stud_email'],
                                                    password=self.mock_data['stud_password'])
        self.supervisor = models.User.objects.create_user(email=self.mock_data['super_email'],
                                                          password=self.mock_data['super_password'])
        self.reviewer = models.User.objects.create_user(email=self.mock_data['rev_email'],
                                                        password=self.mock_data['rev_password'])
        # Assigning users to user groups
        supervisors.user_set.add(self.supervisor)
        students.user_set.add(self.stud)
        reviewers.user_set.add(self.reviewer)
        # Creating a topic, thesis and review
        self.topic = models.Topic.objects.create(name=self.mock_data['topic_name'],
                                                 short_description=self.mock_data['topic_desc'],
                                                 student=self.stud,
                                                 supervisor=self.supervisor)
        self.thesis = models.Thesis.objects.create(topic=self.topic, student=self.stud,
                                                   supervisor=self.supervisor, finished=True)
        self.review = models.Review.objects.create(thesis=self.thesis, author=self.reviewer)
        self.media_root = settings.MEDIA_ROOT
        settings.MEDIA_ROOT = 'test/'
        self.client = Client()

    def test_student_can_propose_topic(self):
        # We have to use mock_data to get password, since self.reviewer.password returns hash
        self.client.login(username=self.reviewer.email, password=self.mock_data['rev_password'])
        form_data = {}
        with open('files/test_review_file.doc', 'rb') as f:
            form_data['review_file'] = f
            form_data['review_hidden_id'] = self.review.id,
            self.client.post(reverse('reviews'), form_data)
        try:
            self.review = models.Review.objects.filter(author=self.reviewer)[0]
        except IndexError:
            self.fail()
        self.assertEqual(ntpath.basename(self.review.file.name), 'review.doc')
        self.assertEqual(self.review.finished, True)
        self.assertEqual(self.review.finished_date.date(), timezone.now().date())

    def tearDown(self):
        shutil.rmtree(settings.MEDIA_ROOT)
        settings.MEDIA_ROOT = self.media_root
