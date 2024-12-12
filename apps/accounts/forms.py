from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django_recaptcha.fields import ReCaptchaField

from .models import Profile


class UserUpdateForm(forms.ModelForm):
    """
    Форма для обновления пользователя
    """
    username = forms.CharField(required=False, max_length=100, widget=forms.TextInput(attrs={"class": "form-control mb-1"}))
    email = forms.EmailField(required=False, widget=forms.TextInput(attrs={"class": "form-control mb-1"}))
    first_name = forms.CharField(required=False, max_length=40, widget=forms.TextInput(attrs={"class": "form-control mb-1"}))
    last_name = forms.CharField(required=False, max_length=50, widget=forms.TextInput(attrs={"class": "form-control mb-1"}))

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name")


class ProfileUpdateForm(forms.ModelForm):
    """
    Форма для обновления профиля
    """
    slug = forms.CharField(max_length=80, widget=forms.TextInput(attrs={"class": "form-control mb-1"}))
    birth_date = forms.DateField(widget=forms.TextInput(attrs={"class": "form-control mb-1", "type": "date"}))
    bio = forms.CharField(max_length=500, widget=forms.Textarea(attrs={"class": "form-control mb-1"}))
    avatar = forms.ImageField(widget=forms.FileInput(attrs={"class": "form-control mb-1"}))

    class Meta:
        model = Profile
        fields = ("slug", "birth_date", "bio", "avatar")


class UserRegisterForm(UserCreationForm):
    """
    Форма для регистрации пользователя
    """
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email', 'first_name', 'last_name')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError('Этот email уже используется')
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'username': "Придумайте логин",
            'first_name': "Ваше имя",
            'last_name': "Ваша фамилия",
            'email': "Введите email",
            'password1': "Придумайте свой пароль",
            'password2': "Повторите придуманный пароль",
        }
        for field, placeholder in placeholders.items():
            self.fields[field].widget.attrs.update({
                "class": "form-control",
                "placeholder": placeholder,
                "autocomplete": "off"
            })


class UserLoginForm(AuthenticationForm):
    recaptcha = ReCaptchaField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            "placeholder": "Логин пользователя",
            "class": "form-control"
        })
        self.fields['password'].widget.attrs.update({
            "placeholder": "Пароль пользователя",
            "class": "form-control"
        })
        self.fields['username'].label = 'Логин'
