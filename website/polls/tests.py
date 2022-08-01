from django.test import TestCase, Client
from polls.models import Question, Choice
from django.contrib.auth import get_user_model, authenticate
from django.urls import reverse
from django.utils import timezone


User = get_user_model()


class UserTestCases(TestCase):
    def test_user_create(self):
        username = "test_username"
        password = "test_password"
        user = User.objects.create(username=username)
        user.set_password(password)
        user.save()
        c = User.objects.count()
        self.assertEqual(c, 1)

        user_auth = authenticate(username=username, password=password)
        self.assertEqual(user_auth, user)


class QuestionTestCases(TestCase):
    def setUp(self):
        self.user_1 = User.objects.create(username="testuser")
        self.user_1.set_password("password")
        self.user_1.save()
        self.client.login(username="testuser", password="password")

    def test_index_view(self):
        res = self.client.get(reverse("polls:index"))
        self.assertEqual(res.status_code, 200)
        # print(res.context.get('questions'))

    def test_question_add_not_authenticated_fail(self):
        payload = {"title": "question"}
        res = self.client.post(reverse("polls:question_create"), payload)
        self.assertEqual(res.status_code, 302)
        c = Question.objects.count()
        self.assertEqual(c, 1)

    def test_question_list_less_than_five(self):
        res = self.client.get(reverse("polls:index"))
        for i in range(6):
            Question.objects.create(title=str(i), user=self.user_1)
        self.assertEqual(res.status_code, 200)
        self.assertLessEqual(len(res.context["questions"]), 5)  # type: ignore

    def test_question_details_view(self):
        question = Question.objects.create(title="test_question", user=self.user_1)
        res = self.client.get(reverse("polls:question_details", args=[question.pk]))  # type: ignore
        self.assertTrue(res.status_code, 200)
        self.assertEqual(res.context.get("question"), question)  # type: ignore


class QuestionModelTest(TestCase):
    def setUp(self):
        self.user_1 = User.objects.create(username="testuser")
        self.user_1.set_password("password")
        self.user_1.save()

    def test_question_is_recent(self):
        old_time = (timezone.now() - timezone.timedelta(days=2)).date()
        old_question = Question.objects.create(title="old q", user=self.user_1)
        old_question.pub_date = old_time
        old_question.save()
        self.assertFalse(old_question.is_recent())
        new_question = Question.objects.create(title="new q", user=self.user_1)
        self.assertTrue(new_question.is_recent())
        future_time = (timezone.now() + timezone.timedelta(days=2)).date()
        future_question = Question.objects.create(
            title="future q", user=self.user_1, pub_date=future_time
        )
        self.assertTrue(future_question.is_recent())
