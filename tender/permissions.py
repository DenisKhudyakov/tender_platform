from functools import wraps

from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponseForbidden


class IsEmployerMixin(UserPassesTestMixin):
    """
    Права доступа только для авторизованных пользователей и сотрудников, для CBV
    """
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_employer


def employer_required(view_func):
    """
    Права доступа только для авторизованных пользователей и сотрудников, для FBV
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not (request.user.is_authenticated and request.user.is_employer):
            return HttpResponseForbidden("Доступ запрещён: только для сотрудников.")
        return view_func(request, *args, **kwargs)

    return _wrapped_view
