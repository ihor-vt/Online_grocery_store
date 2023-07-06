from django.urls import path
from django.contrib.auth.views import (
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)

from . import views

app_name = "users"

urlpatterns = [
    path("login/", views.login, name="login"),
    path("register/", views.registration, name="registration"),
    path("logout/", views.logoutuser, name="logout"),
    path("inform/", views.add_user_information, name="add_user_information"),
    path(
        "check-user/", views.check_full_user_data, name="check_full_user_data"
    ),
    path(
        "edit/<int:user_id>",
        views.edit_user_information,
        name="edit_user_information",
    ),
    path("user/<int:user_id>", views.specific_user, name="specific_user"),
    path(
        "reset-password/",
        views.ResetPasswordView.as_view(),
        name="password_reset",
    ),
    path(
        "reset-password/done/",
        PasswordResetDoneView.as_view(
            template_name="authentication/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset-password/confirm/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(
            template_name="authentication/password_reset_confirm.html",
            success_url="/users/reset-password/complete/",
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset-password/complete/",
        PasswordResetCompleteView.as_view(
            template_name="authentication/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]
