# Импортируем из приложения django.contrib.auth нужный view-класс
from django.contrib.auth.views import (LoginView, LogoutView,
                                       PasswordChangeDoneView,
                                       PasswordChangeView,
                                       PasswordResetCompleteView,
                                       PasswordResetConfirmView,
                                       PasswordResetView)
from django.urls import path

from . import views

app_name = "users"

urlpatterns = [
    path(
        "logout/",
        # Прямо в описании обработчика укажем шаблон,
        # который должен применяться для отображения возвращаемой страницы.
        # Да, во view-классах так можно! Как их не полюбить.
        LogoutView.as_view(template_name="users/logged_out.html"),
        name="logout",
    ),
    # Полный адрес страницы регистрации - auth/signup/,
    # но префикс auth/ обрабатывется в головном urls.py
    path("signup/", views.SignUp.as_view(), name="signup"),
    path(
        "login/",
        LoginView.as_view(template_name="users/login.html"),
        name="login",
    ),
    path(
        "password_reset_form/",
        PasswordResetView.as_view(
            template_name="users/password_reset_form.html"
        ),
        name="password_reset_form",
    ),
    path(
        "password_change/",
        PasswordChangeView.as_view(
            template_name="users/password_change_form.html"
        ),
        name="password_change",
    ),
    path(
        "password_change/done/",
        PasswordChangeDoneView.as_view(
            template_name="users/password_change_done.html"
        ),
        name="password_change_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(
            template_name="users/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    # восстановление пароля: уведомление что пароль изменен
    path(
        "reset/done/",
        PasswordResetCompleteView.as_view(
            template_name="users/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]
