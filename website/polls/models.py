from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Question(models.Model):
    title = models.TextField()
    pub_date = models.DateField(auto_now_add=True)
    mod_date = models.DateField(auto_now=True)

    def __str__(self) -> str:
        return f"Question({self.title[:10]}...)"

    class Meta:
        ordering = ["-pub_date"]


class Choice(models.Model):
    title = models.CharField(max_length=128)
    question = models.ForeignKey(
        Question, related_name="choices", on_delete=models.CASCADE
    )
    users = models.ManyToManyField(User, related_name="votes", blank=True)

    def __str__(self) -> str:
        return f"Choice({self.title[:5]}...)"

    @property
    def num_votes(self):
        return len(self.users)
