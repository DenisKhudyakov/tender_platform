from django.contrib.auth.views import LogoutView
from django.urls import path

from users import views
from users.apps import UsersConfig
from users.views import UserCreate, UserLogin, main

app_name = UsersConfig.name

urlpatterns = [
    path("login/", UserLogin.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", UserCreate.as_view(), name="register"),
    path('main/', main, name='main'),
]
