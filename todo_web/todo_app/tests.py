from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Task
from .forms import ScheduleTaskForm, SignUpForm


# Create your tests here.
class TestScheduleTask(TestCase):
    def setUp(self):
        # create a user
        self.test_user1 = User.objects.create(
            username='testuser1', first_name="Testuser1", last_name="Testuser1",
            email="testuser1@test.com", password='1X<ISRUkw+tuK')
        # create a task
        self.test_task1 = Task.objects.create(
            title="Test_task1", description="Test_task1",
            expire_at="2023-09-16 08:16:46+00:00", user_id=self.test_user1)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('schedule_task'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login'))

    def test_is_schedule_form_valid(self):
        #schedule form validation
        user = User.objects.create_user(username='testuser2', password='pass123456')
        self.client.login(username='testuser2', password='pass123456')

        response = self.client.post(reverse('schedule_task'), {
            'title': 'Test Title',
            'description': 'Test Description',
            'expire_at': timezone.now() + timedelta(days=7)
        })
        self.assertEqual(response.status_code, 302)  # status code 302 due to redirect
        self.assertRedirects(response, reverse('dashboard'))

    def test_date_not_given(self):
        # schedule form validation
        form = ScheduleTaskForm(data={})
        form_data = {
            'title': 'Test Title',
            'description': 'Test Description'
        }
        form = ScheduleTaskForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_invalid_date_given(self):
        # schedule form validation
        form = ScheduleTaskForm(data={})
        form_data = {
            'title': 'Test Title',
            'description': 'Test Description',
            'expire_at': datetime.now() - timedelta(days=7),
        }
        form = ScheduleTaskForm(data=form_data)
        self.assertFalse(form.is_valid())


class TestGetTask(TestCase):
    def setUp(self):
        # create a user
        test_user3 = User.objects.create_user(username='testuser3', password='3HJ1vRV0Z&3iD')
        test_user3.save()
        # create a task
        self.test_task3 = Task.objects.create(
            title="Test_task3", description="Test_task3",
            expire_at="2023-09-16 08:16:46+00:00", user_id=test_user3)
        test_user6 = User.objects.create_user(username='testuser6', password='6HJ1vRV0Z&3iD')
        test_user6.save()

    def test_view_url_exists_at_desired_location(self):
        self.client.login(username='testuser3', password='3HJ1vRV0Z&3iD')
        response = self.client.get('/task/' + str(self.test_task3.pk))
        self.assertEqual(response.status_code, 200)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('task', kwargs={'pk': self.test_task3.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login'))

        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login'))

    def test_get_task_by_id(self):
        self.client.login(username='testuser3', password='3HJ1vRV0Z&3iD')
        response = self.client.get(reverse('task', kwargs={'pk': self.test_task3.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('task' in response.context)
        self.assertEqual(response.context['task'], self.test_task3)

    def test_invalid_id(self):
        self.client.login(username='testuser3', password='3HJ1vRV0Z&3iD')
        response = self.client.get('/task/' + str(10))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('dashboard'))

    def test_get_dashboard_with_tasks(self):
        self.client.login(username='testuser3', password='3HJ1vRV0Z&3iD')
        response = self.client.get(reverse('dashboard'))
        self.assertNotEquals(len(response.context['tasks']), 0)

    def test_empty_dashboard(self):
        self.client.login(username='testuser6', password='6HJ1vRV0Z&3iD')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(len(response.context['tasks']), 0)


class TestDeleteTask(TestCase):
    def setUp(self):
        # create a user
        test_user3 = User.objects.create_user(username='testuser3', password='3HJ1vRV0Z&3iD')
        test_user3.save()
        # create a task
        self.test_task3 = Task.objects.create(
            title="Test_task3", description="Test_task3",
            expire_at="2023-09-16 08:16:46+00:00", user_id=test_user3)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('delete_task', kwargs={'pk': self.test_task3.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login'))

    def test_check_task_deletion(self):
        self.client.login(username='testuser3', password='3HJ1vRV0Z&3iD')
        response = self.client.get('/delete_task/' + str(self.test_task3.pk))
        self.assertEqual(response.status_code, 302)
        # after deletion redirects to dashbaord
        self.assertRedirects(response, reverse('dashboard'))

    def test_invalid_id(self):
        self.client.login(username='testuser3', password='3HJ1vRV0Z&3iD')
        response = self.client.get('/delete_task/' + str(10))
        # after deletion redirects to dashbaord
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('dashboard'))

    def test_negative_id(self):
        self.client.login(username='testuser3', password='3HJ1vRV0Z&3iD')
        response = self.client.get('/delete_task/' + str(-1))
        self.assertEqual(response.status_code, 404)


class TestUpdateTask(TestCase):
    def setUp(self):
        # create a user
        test_user3 = User.objects.create_user(username='testuser3', password='3HJ1vRV0Z&3iD')
        test_user3.save()
        # create a task
        self.test_task3 = Task.objects.create(
            title="Test_task3", description="Test_task3",
            expire_at="2023-09-16 08:16:46+00:00", user_id=test_user3)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('mark_task', kwargs={'pk': self.test_task3.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login'))

        response = self.client.get(reverse('update_task', kwargs={'pk': self.test_task3.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login'))

    def test_mark_status_complete(self):
        self.client.login(username='testuser3', password='3HJ1vRV0Z&3iD')

        response = self.client.post(reverse('mark_task', kwargs={'pk': self.test_task3.pk}), {
            'new_status': 'Completed'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue('task' in response.context)
        self.assertEqual(response.context['task'].status, "Completed")

    def test_invalid_task(self):
        self.client.login(username='testuser3', password='3HJ1vRV0Z&3iD')
        response = self.client.post(reverse('mark_task', kwargs={'pk': str(10)}), {
            'new_status': 'Completed'
        })
        self.assertEqual(response.status_code, 404)

    def test_valid_update(self):
        self.client.login(username='testuser3', password='3HJ1vRV0Z&3iD')
        response = self.client.post(reverse('update_task', kwargs={'pk': self.test_task3.pk}), {
            "title": "Test title 3"
        })
        self.assertEqual(response.context['task'].title, "Test title 3")
        self.assertEqual(response.status_code, 200)

    def test_invalid_update_id(self):
        self.client.login(username='testuser3', password='3HJ1vRV0Z&3iD')
        response = self.client.get(reverse('update_task', kwargs={'pk': str(10)}))
        self.assertEqual(response.status_code, 404)


class TestUserAuthentication(TestCase):
    def setUp(self):
        # create a user
        test_user4 = User.objects.create_user(username='testuser4', password='4HJ1vRV0Z&3iD')
        test_user4.save()
        # create a task
        self.test_task4 = Task.objects.create(
            title="Test_task4", description="Test_task4",
            expire_at="2023-09-16 08:16:46+00:00", user_id=test_user4)

    def test_successful_login(self):
        response = self.client.post(reverse('login'), {
            "username": 'testuser4',
            "password": '4HJ1vRV0Z&3iD'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/dashboard/'))
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_login_wrong_password(self):
        response = self.client.post(reverse('login'), {
            "username": 'testuser4',
            "password": '3iD78788'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login/'))

    def test_logout(self):
        self.client.login(username='testuser4', password='4HJ1vRV0Z&3iD')
        self.assertTrue('_auth_user_id' in self.client.session)  # session true before logout
        res = self.client.get(reverse("logout"))
        self.assertFalse('_auth_user_id' in self.client.session)  # session false after logout
        self.assertEqual(res.status_code, 302)
        self.assertTrue(res.url.startswith('/'))

    def test_if_already_logged_out(self):
        res = self.client.get(reverse("logout"))
        self.assertFalse('_auth_user_id' in self.client.session)  # session false as already logged out
        self.assertEqual(res.status_code, 302)
        self.assertTrue(res.url.startswith('/login/'))

    def test_redirect_if_logged_in(self):
        #signup not allowed if already logged in
        self.client.login(username='testuser4', password='4HJ1vRV0Z&3iD')
        res = self.client.get(reverse("signup"))
        self.assertEqual(res.status_code, 302)
        self.assertTrue(res.url.startswith('/dashboard/'))

    def test_successful_signup(self):
        response = self.client.post(reverse('signup'), {
            "username": 'testuser5',
            "first_name": "test",
            "last_name": "user5",
            "email": "user5@test.com",
            "password1": '5iD78788',
            "password2": '5iD78788',
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('dashboard'))
        #after signup, user will be logged in
        self.assertTrue('_auth_user_id' in self.client.session)
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_invalid_username(self):
        #username already exists
        response = self.client.post(reverse('signup'), {
            "username": 'testuser4',
            "first_name": "test",
            "last_name": "user4",
            "email": "user4@test.com",
            "password1": '4iD78788',
            "password2": '4iD78788',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['form'].is_valid())

    def test_different_passwords(self):
        # signup form validation: password1 and password2 are different
        form = SignUpForm(data={})
        form_data = {
            "username": 'testuser6',
            "first_name": "test",
            "last_name": "user6",
            "email": "user6@test.com",
            "password1": '4iE78788',
            "password2": '4iD78788',
        }
        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())

