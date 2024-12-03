from django import forms
from django.contrib.auth.models import User
from .models import Profile


class UserUpdateForm(forms.ModelForm):
    """
    Форма для обновления пользователя
    """
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"class":"form-control mb-1"}))
    email = forms.EmailField(widget=forms.TextInput(attrs={"class":"form-control mb-1"}))
    first_name = forms.CharField(max_length=40, widget=forms.TextInput(attrs={"class": "form-control mb-1"}))
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={"class":"form-control mb-1"}))

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name")


class ProfileUpdateForm(forms.ModelForm):
    """
    форма для обновления form
    """
    slug = forms.CharField(max_length=80, widget=forms.TextInput(attrs={"class":"form-control mb-1"}))
    birth_date = forms.DateTimeField(widget=forms.TextInput(attrs={"class":"form-control mb-1"}))
    bio = forms.CharField(max_length=500, widget=forms.Textarea(attrs={"class":"form-control mb-1"}))
    avatar = forms.ImageField(widget=forms.FileInput(attrs={"class":"form-control mb-1"}))


    class Meta:
        model = Profile
        fields = ("slug", "birth_data", "bio", "avatar")


