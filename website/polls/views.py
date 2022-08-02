from __future__ import annotations
from django.shortcuts import render, redirect, get_object_or_404
from polls.models import Question, Choice, User
from polls.forms import (
    ChoiceCreateForm,
    QuestionCreateForm,
    UserCreateForm,
    UserLoginForm,
    UserUpdateForm,
)
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views import generic


def handle_404_view(request, exception: Exception):
    print(exception)
    return render(request, "404.html")


def index_view(request, q: str | None = None):
    questions = Question.objects.all()
    q = request.GET.get("q")
    if q:
        questions = questions.filter(title__icontains=q)
    context = {"questions": questions[:5]}
    return render(request, "index.html", context=context)


class UserListView(generic.ListView):
    model = User
    template_name = "user_list.html"
    context_object_name = "users"


def user_create_view(request):
    if request.user.is_authenticated:
        return redirect("polls:index")
    form = UserCreateForm(request.POST, request.FILES or None)
    if request.method == "POST":
        if form.is_valid():
            password = form.cleaned_data.pop("confirm_password")
            user = User.objects.create(**form.cleaned_data)
            user.set_password(password)
            user.save()
            login(request, user)
            messages.add_message(request, messages.SUCCESS, "Account was created.")
            return redirect("polls:index")
        else:
            messages.add_message(request, messages.ERROR, "Invalid Data.")
            return redirect("polls:user_create")
    context = {"form": form}
    return render(request, "user_create.html", context=context)


@login_required(login_url=reverse_lazy("polls:user_login"))
def user_update_view(request, username: str):
    user = get_object_or_404(User, username=username)
    if request.user != user:
        messages.add_message(
            request, messages.ERROR, "You can only update your own profile!"
        )
        return redirect("polls:index")
    form = UserUpdateForm(request.POST, request.FILES or None)
    if request.method == "POST":
        if form.is_valid():
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            email = form.cleaned_data.get("email")
            image = form.cleaned_data.get("image")
            password = form.cleaned_data.get("password")
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.image = image
            if password:
                user.set_password(password)
            user.save()
            return redirect("polls:user_details", username=user.username)
        else:
            messages.add_message(request, messages.ERROR, "Invalid data.")

    initial_data = {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
    }
    form = UserUpdateForm(initial=initial_data)
    context = {"form": form}
    return render(request, "user_update.html", context=context)


def user_login_view(request):
    if request.user.is_authenticated:
        return redirect("polls:index")
    form = UserLoginForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data.get("username"),
                password=form.cleaned_data.get("password"),
            )
            if user:
                login(request, user)
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    f"Logged in as `{form.cleaned_data.get('username')}`",
                )
                return redirect("polls:index")
            else:
                messages.add_message(request, messages.ERROR, "Invalid user data.")
        else:
            messages.add_message(request, messages.ERROR, "Invalid user data.")

    context = {"form": form}
    return render(request, "user_login.html", context=context)


@login_required(login_url=reverse_lazy("polls:user_login"))
def user_logout_view(request):
    if not request.user.is_authenticated:
        return redirect("polls:user_login")
    if request.method == "POST":
        if request.user.is_authenticated:
            logout(request)
            messages.add_message(request, messages.SUCCESS, "Logget out successfully.")
            return redirect("polls:index")
    return render(request, "user_logout.html")


def user_details_view(request, username: str):
    user = get_object_or_404(User, username=username)
    context = {"user": user}
    return render(request, "user_details.html", context=context)


@login_required(login_url=reverse_lazy("polls:user_login"))
def question_create_view(request):
    form = QuestionCreateForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            question = Question.objects.create(
                title=form.cleaned_data.get("title"), user=request.user
            )
            messages.add_message(
                request, messages.SUCCESS, "Question was created successfully."
            )
            return redirect("polls:question_details", pk=question.pk)
        else:
            messages.add_message(request, messages.ERROR, "Invalid data.")
    context = {"form": form}
    return render(request, "question_create.html", context=context)


class QuestionDetailView(generic.DetailView):
    model = Question
    template_name = "question_details.html"
    context_object_name = "question"


@login_required(login_url=reverse_lazy("polls:user_login"))
def question_submit_view(request, pk: int):
    if pk in request.session.get("voted", []):
        messages.add_message(
            request, messages.ERROR, "You have already voted for this Question."
        )
        return redirect("polls:question_details", pk=pk)
    question = get_object_or_404(Question, pk=pk)
    if request.method == "POST":
        choice_pk = request.POST.get("choice")
        if choice_pk is None:
            messages.add_message(request, messages.ERROR, "No votes was submitted.")
            return redirect("polls:question_details", pk=question.pk)
        choice = get_object_or_404(Choice, pk=choice_pk)
        choice.users.add(request.user)
        choice.save()
        request.session["voted"] = request.session.get("voted", []) + [pk]
        messages.add_message(request, messages.SUCCESS, "Voted submitted. Thanks!")
    context = {"question": question}
    return render(request, "question_submit.html", context=context)


@login_required(login_url=reverse_lazy("polls:user_login"))
def choice_create_view(request, question_id: int):
    form = ChoiceCreateForm(request.POST or None)
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        choice_title = request.POST.get("choice")
        choice = Choice.objects.create(title=choice_title, question=question)
        messages.add_message(
            request,
            messages.SUCCESS,
            f"Choice `{choice.title}` was added successfully.",
        )
        return redirect("polls:question_details", pk=question_id)
    context = {"form": form, "question": question}
    return render(request, "choice_create.html", context=context)
