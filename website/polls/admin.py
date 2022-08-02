from django.contrib import admin
from django.contrib.auth.admin import UserAdmin  # type: ignore
from polls.models import Choice, Question, User


class UserAdmin(UserAdmin):
    model = User
    list_display = [
        "id",
        "email",
        "username",
    ]


class QuestionAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "user"]


class ChoiceAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "question"]


admin.site.register(User, UserAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)
