from django import forms
from django.contrib.auth import get_user_model
from polls.models import Question, Choice, User


class UserCreateForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ["username", "email", "password", "image"]

    def clean(self):
        cleaned_data = super(UserCreateForm, self).clean()
        password = cleaned_data.get("password")  # type: ignore
        confirm_password = cleaned_data.get("confirm_password")  # type: ignore

        if password != confirm_password:
            raise forms.ValidationError("password and confirm_password does not match")


class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=128)
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super(UserLoginForm, self).clean()
        password = cleaned_data.get("password")  # type: ignore
        confirm_password = cleaned_data.get("confirm_password")  # type: ignore
        if password != confirm_password:
            raise forms.ValidationError("password and confirm_password does not match")


class UserUpdateForm(forms.Form):
    first_name = forms.CharField(max_length=128, required=False)
    last_name = forms.CharField(max_length=128, required=False)
    email = forms.EmailField(max_length=256)
    password = forms.CharField(widget=forms.PasswordInput(), required=False)
    confirm_password = forms.CharField(widget=forms.PasswordInput(), required=False)
    image = forms.ImageField(required=False)

    def clean(self):
        cleaned_data = super(UserUpdateForm, self).clean()
        password = cleaned_data.get("password")  # type: ignore
        confirm_password = cleaned_data.get("confirm_password")  # type: ignore
        if password != confirm_password:
            raise forms.ValidationError("password and confirm_password does not match")


class QuestionCreateForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ["title"]


class ChoiceCreateForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ["title", "question"]
