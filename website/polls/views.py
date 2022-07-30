from __future__ import annotations
from django.shortcuts import render, redirect, get_object_or_404
from polls.models import Question, Choice
from polls.forms import (
    ChoiceCreateForm,
    QuestionCreateForm,
    UserCreateForm,
    UserLoginForm,
)
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def index_view(request, q: str | None = None):
    questions = Question.objects.all()
    if request.method == "POST":
        q = request.POST.get("q")
        questions = questions.filter(title__icontains=q)
    context = {"questions": questions}
    return render(request, "index.html", context=context)


def user_create_view(request):
    form = UserCreateForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            password = form.cleaned_data.get("password")
            user = form.save()
            user.set_password(password)
            login(request, user)
            messages.add_message(request, messages.SUCCESS, "Account was created.")
        else:
            messages.add_message(request, messages.ERROR, "Invalid Data.")
            return redirect("polls:user_create")
    context = {"form": form}
    return render(request, "index.html", context=context)


def user_login_view(request):
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
                    f"Logged in as {form.cleaned_data.get('username')}",
                )
                return redirect("polls:index")
            else:
                messages.add_message(request, messages.ERROR, "Invalid user data.")
        else:
            messages.add_message(request, messages.ERROR, "Invalid user data.")
    context = {"form": form}
    return render(request, "user_login.html", context=context)


def question_create_view(request):
    form = QuestionCreateForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            question = form.save()
            messages.add_message(
                request, messages.SUCCESS, "Question was created successfully."
            )
        else:
            messages.add_message(request, messages.ERROR, "Invalid data.")
    context = {"form": form}
    return render(request, "question_create.html", context=context)


def question_details_view(request, pk: int):
    question = get_object_or_404(Question, pk=pk)
    context = {"question": question}
    return render(request, "question_details.html", context=context)


def choice_create_view(request):
    form = ChoiceCreateForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            choice = form.save()
            messages.add_message(
                request, messages.SUCCESS, "Choice was created successfully."
            )
        else:
            messages.add_message(request, messages.ERROR, "Invalid data.")
    context = {"form": form}
    return render(request, "index.html", context=context)
