from django.urls import path
from polls import views

handler404 = "polls.views.handle_404_view"

app_name = "polls"
urlpatterns = [
    path("", views.index_view, name="index"),
    path("auth/create", views.user_create_view, name="user_create"),
    path("auth/login", views.user_login_view, name="user_login"),
    path("auth/logout", views.user_logout_view, name="user_logout"),
    path("users/", views.UserListView.as_view(), name="user_list"),
    path("users/<str:username>/profile", views.user_details_view, name="user_details"),
    path("users/<str:username>/update", views.user_update_view, name="user_update"),
    path("questions/create", views.question_create_view, name="question_create"),
    path(
        "questions/<int:pk>/",
        views.QuestionDetailView.as_view(),
        name="question_details",
    ),
    path(
        "questions/<int:pk>/submit", views.question_submit_view, name="question_submit"
    ),
    path(
        "questions/<int:question_id>/choice-create",
        views.choice_create_view,
        name="choice_create",
    ),
]
