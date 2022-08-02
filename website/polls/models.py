import os
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.dispatch import receiver
from polls.utils import uuid_namer


class User(AbstractUser):
    image = models.ImageField(blank=True, null=True, upload_to=uuid_namer)

    def __str__(self) -> str:
        return f"User({self.username})"


class Question(models.Model):
    title = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pub_date = models.DateField(auto_now_add=True)
    mod_date = models.DateField(auto_now=True)

    class Meta:
        ordering = ["-pub_date"]

    def is_recent(self) -> bool:
        return (
            self.pub_date >= (timezone.now() - timezone.timedelta(days=1)).date()
            and self.pub_date <= timezone.now().date()
        )

    def __str__(self) -> str:
        return f"Question({self.title[:10]}...)"


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


@receiver(models.signals.post_delete, sender=User)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes image from filesystem
    when corresponding `User` object is deleted.
    """
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)


@receiver(models.signals.pre_save, sender=User)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old image from filesystem
    when corresponding `User` object is updated
    with new image.
    """
    if not instance.pk:
        return False

    try:
        old_file = User.objects.get(pk=instance.pk).image
    except User.DoesNotExist:
        return False

    new_file = instance.image
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)
