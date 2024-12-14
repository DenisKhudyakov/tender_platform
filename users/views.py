from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from users.forms import LoginForm, SignUpForm


def main(request):
    """
    Отображение главной страница
    """
    return render(request, "users/main.html")


class UserLogin(LoginView):
    """
    Контроллер авторизации
    """

    form_class = LoginForm
    template_name = "users/authorization.html"


class UserCreate(CreateView):
    """
    Контроллер регистрации пользователя
    """

    template_name = "users/registration.html"
    form_class = SignUpForm
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        user = form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Регистрация на сайте"
        return context
