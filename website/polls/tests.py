from django.test import TestCase
from polls.models import Question, Choice, User
from django.contrib.auth import get_user_model, authenticate
from django.urls import reverse
from django.utils import timezone


class UserModelTestCases(TestCase):
    def test_user_create_success(self):
        username = "test_username"
        password = "test_password"
        user = User.objects.create(username=username)
        user.set_password(password)
        user.save()
        c = User.objects.count()
        self.assertEqual(c, 1)

        user_auth = authenticate(username=username, password=password)
        self.assertEqual(user_auth, user)

    def test_user_create_invalid_data_fail(self):
        pass


class QuestionViewTestCases(TestCase):
    def setUp(self):
        self.user_1 = User.objects.create(username="testuser")
        self.user_1.set_password("password")
        self.user_1.save()
        self.client.login(username="testuser", password="password")

    def test_index_view(self):
        res = self.client.get(reverse("polls:index"))
        self.assertEqual(res.status_code, 200)
        # print(res.context.get('questions'))

    def test_question_add_authenticated_success(self):
        payload = {"title": "question"}
        res = self.client.post(reverse("polls:question_create"), payload)
        self.assertEqual(res.status_code, 302)  # Redirects to index page.
        c = Question.objects.count()
        self.assertEqual(c, 1)

    def test_index_question_list_less_than_five(self):
        res = self.client.get(reverse("polls:index"))
        for i in range(6):
            Question.objects.create(title=str(i), user=self.user_1)
        self.assertEqual(res.status_code, 200)
        self.assertLessEqual(len(res.context["questions"]), 5)  # type: ignore

    def test_question_details_view(self):
        question = Question.objects.create(title="test_question", user=self.user_1)
        res = self.client.get(reverse("polls:question_details", args=[question.pk]))
        self.assertTrue(res.status_code, 200)
        self.assertEqual(res.context.get("question"), question)  # type: ignore


class QuestionModelTest(TestCase):
    def setUp(self):
        self.user_1 = User.objects.create(username="testuser")
        self.user_1.set_password("password")
        self.user_1.save()

    def test_old_question_is_recent_false(self):
        old_time = (timezone.now() - timezone.timedelta(days=2)).date()
        old_question = Question.objects.create(title="old q", user=self.user_1)
        old_question.pub_date = old_time
        old_question.save()
        self.assertFalse(old_question.is_recent())

    def test_new_question_is_recent_true(self):
        new_question = Question.objects.create(title="new q", user=self.user_1)
        self.assertTrue(new_question.is_recent())

    def test_future_question_is_recent_false(self):
        future_time = (timezone.now() + timezone.timedelta(days=2)).date()
        future_question = Question.objects.create(title="future q", user=self.user_1)
        future_question.pub_date = future_time
        future_question.save()
        self.assertFalse(future_question.is_recent())
