from django.test import TestCase, Client
from django.urls import reverse
import unittest.mock
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
        stud = models.User.objects.create_user(email=self.mock_data['stud_email'],
                                               password=self.mock_data['stud_password'])
        supervisor = models.User.objects.create_user(email=self.mock_data['super_email'],
                                                     password=self.mock_data['super_password'])
        supervisors.user_set.add(supervisor)
        students.user_set.add(stud)
        self.stud = stud
        self.supervisor = supervisor
        self.client = Client()

    def test_student_can_propose_topic(self):
        self.client.login(username=self.stud.email, password=self.stud.password)
        self.client.post(reverse('topic_list'),
                         {
                             'name': self.mock_data['topic_name'],
                             'description': self.mock_data['topic_desc'],
                             'supervisor': self.supervisor.id
                         })
        print(models.Topic.objects.all())
        print(self.supervisor.id)
        proposed_topic = models.Topic.objects.filter(student__id=self.stud.id)
        print(proposed_topic)
        self.assertTrue(proposed_topic is not None)
        self.assertEqual(proposed_topic.name, self.mock_data['topic_name'])
        self.assertEqual(proposed_topic.short_description, self.mock_data['topic_desc'])
        self.assertEqual(proposed_topic.supervisor, self.supervisor)
        self.assertEqual(proposed_topic.student, self.stud)
