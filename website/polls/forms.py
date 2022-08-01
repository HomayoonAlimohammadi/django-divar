from django import forms
from django.contrib.auth import get_user_model
from polls.models import Question, Choice


User = get_user_model()


class UserCreateForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def clean(self):
        cleaned_data = super(UserCreateForm, self).clean()
        password = cleaned_data.get("password")  # type: ignore
        confirm_password = cleaned_data.get("confirm_password")  # type: ignore

        if password != confirm_password:
            raise forms.ValidationError("password and confirm_password does not match")


class UserLoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ["username", "password"]

    def clean(self):
        print("i am cleaning")
        cleaned_data = super(UserLoginForm, self).clean()  # type: ignore
        password = cleaned_data.get("password")  # type: ignore
        confirm_password = cleaned_data.get("confirm_password")  # type: ignore
        print(password, confirm_password)
        if password != confirm_password:
            raise forms.ValidationError("password and confirm_password does not match")
        return cleaned_data


class QuestionCreateForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ["title"]


class ChoiceCreateForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ["title", "question"]
