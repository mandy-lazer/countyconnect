from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path(
        "verify-email/",
        views.verify_email,
        name="verify_email",
    ),
    path(
        "verify-login/",
        views.verify_login,
        name="verify_login",
    ),
    path(
        "resend-otp/",
        views.resend_otp,
        name="resend_otp",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(),
        name="logout",
    ),
]