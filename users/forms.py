from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ValidationError

from users.models import User


class SignUpForm(UserCreationForm):
    """
    Форма регистрации пользователя
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if field.help_text:
                field.help_text = f'<span class="text-light">{field.help_text}</span>'

    email = forms.EmailField(
        max_length=255,
        help_text="Введите электронную почту. Обязательное поле.",
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Логин"}
        ),
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Введите пароль"}
        ),
        label="Пароль",
        help_text="Введите пароль длиной не менее 8 символов",
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Подтвердите пароль"}
        ),
        label="Подтверждение пароля",
    )

    class Meta:
        model = User
        fields = ("email", "company_name", "phone", "inn", "password1", "password2")
        widgets = {
            "company_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Название компании"}
            ),
            "phone": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Номер телефона"}
            ),
            "inn": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "ИНН"}
            ),
        }

    def clean_confirm_password(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 != password2:
            raise ValidationError("Пароли не совпадают")
        return password2


class LoginForm(AuthenticationForm):
    """
    Форма авторизации пользователя
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if field.help_text:
                field.help_text = f'<span class="text-light">{field.help_text}</span>'

    username = forms.CharField(
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Логин"}
        ),
        label="Адрес электронной почты",
        help_text="Введите электронную почту",
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Пароль"}
        ),
        help_text="Введите пароль",
    )
