from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Question(models.Model):
    title = models.TextField()
    users = models.ManyToManyField(
        User, null=True, blank=True, related_name="questions"
    )

    def __str__(self) -> str:
        return f"Question({self.title[:10]}...)"


class Choice(models.Model):
    title = models.CharField(max_length=128)
    question = models.ForeignKey(
        Question, related_name="choices", on_delete=models.CASCADE
    )

    def __str__(self) -> str:
        return f"Choice({self.title[:5]}...)"
