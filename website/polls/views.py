from __future__ import annotations
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from polls.models import Question, Choice
from polls.forms import (
    ChoiceCreateForm,
    QuestionCreateForm,
    UserCreateForm,
    UserLoginForm,
)
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages


User = get_user_model()


def handle_404_view(request, exception):
    return render(request, "404.html")


def index_view(request, q: str | None = None):
    questions = Question.objects.all()
    if request.method == "POST":
        q = request.POST.get("q")
        questions = questions.filter(title__icontains=q)[:5]
    context = {"questions": questions}
    return render(request, "index.html", context=context)


def user_create_view(request):
    form = UserCreateForm(request.POST or None)
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


def user_login_view(request):
    form = UserLoginForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data.get("username"),
                password=form.cleaned_data.get("password"),
            )
            print(form.cleaned_data)
            if user:
                login(request, user)
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    f"Logged in as {form.cleaned_data.get('username')}",
                )
                return redirect("polls:index")
            else:
                messages.add_message(request, messages.ERROR, "Invalid user data.")
        else:
            messages.add_message(request, messages.ERROR, "Invalid user data.")
    context = {"form": form}
    return render(request, "user_login.html", context=context)


def user_logout_view(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            logout(request)
            messages.add_message(request, messages.SUCCESS, "Logget out successfully.")
            return redirect("polls:index")
    return render(request, "user_logout.html")


def question_create_view(request):
    form = QuestionCreateForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            question = form.save()
            messages.add_message(
                request, messages.SUCCESS, "Question was created successfully."
            )
            return redirect("polls:question_details", pk=question.pk)
        else:
            messages.add_message(request, messages.ERROR, "Invalid data.")
    context = {"form": form}
    return render(request, "question_create.html", context=context)


def question_details_view(request, pk: int):
    question = get_object_or_404(Question, pk=pk)
    context = {"question": question}
    return render(request, "question_details.html", context=context)


def question_submit_view(request, pk: int):
    question = get_object_or_404(Question, pk=pk)
    context = {"question": question}
    return render(request, "question_submit.html", context=context)


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
