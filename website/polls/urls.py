from django.urls import path
from polls import views

app_name = "polls"
urlpatterns = [
    path("", views.index_view, name="index"),
    path("auth/create", views.user_create_view, name="user_create"),
    path("auth/login", views.user_login_view, name="user_login"),
    path("questions/create", views.question_create_view, name="question_create"),
    path("questions/<int:pk>/", views.question_details_view, name="question_details"),
    path("choices/create", views.choice_create_view, name="choice_create"),
]
