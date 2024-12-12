from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django_recaptcha.fields import ReCaptchaField

from .models import Profile


class UserUpdateForm(forms.ModelForm):
    """
    Форма для обновления пользователя
    """
    username = forms.CharField(required=False, max_length=100, widget=forms.TextInput(attrs={"class":"form-control mb-1"}))
    email = forms.EmailField(required=False, widget=forms.TextInput(attrs={"class":"form-control mb-1"}))
    first_name = forms.CharField(required=False, max_length=40, widget=forms.TextInput(attrs={"class": "form-control mb-1"}))
    last_name = forms.CharField(required=False, max_length=50, widget=forms.TextInput(attrs={"class":"form-control mb-1"}))

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


class UserRegisterForm(UserCreationForm):
    """
    Тут предопределилили род. класс
    """
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('email', 'first_name', 'last_name')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError('Этот email уже используется')
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({"placeholder": "Придумайте логин"})
        self.fields['first_name'].widget.attrs.update({"placeholder": "Ваше имя"})
        self.fields['last_name'].widget.attrs.update({"placeholder": "Ваша фамилию"})
        self.fields['email'].widget.attrs.update({"placeholder": "Введите email"})
        self.fields['password1'].widget.attrs.update({"placeholder": "Придумайте свой пароль"})
        self.fields['password2'].widget.attrs.update({"placeholder": "Повторите придуманный пароль"})
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control", "autocomplete": "off"})


class UserLoginForm(AuthenticationForm):
    recaptcha = ReCaptchaField()

    class Meta:
        model = User
        fields = ['username', 'password', 'recaptcha']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Логин пользователя'
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['placeholder'] = 'Пароль пользователя'
        self.fields['password'].widget.attrs['class'] = 'form-control'
        self.fields['username'].label = 'Логин'

