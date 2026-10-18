from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    phone_number = models.CharField(
        max_length=15, blank=True,
        help_text="Optional; used for future SMS notifications.",
    )

    @property
    def is_citizen(self):
        return not self.is_staff

    def __str__(self):
        return self.get_full_name() or self.username


import hashlib

from django.conf import settings
from django.db import models
from django.utils import timezone


class EmailOTP(models.Model):
    REGISTRATION = "registration"
    LOGIN = "login"

    PURPOSE_CHOICES = [
        (REGISTRATION, "Registration"),
        (LOGIN, "Login"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="email_otps",
    )
    purpose = models.CharField(max_length=20, choices=PURPOSE_CHOICES)
    code_hash = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    attempts = models.PositiveSmallIntegerField(default=0)
    used_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def set_code(self, code):
        self.code_hash = hashlib.sha256(code.encode()).hexdigest()

    def check_code(self, code):
        return (
            self.code_hash
            == hashlib.sha256(code.encode()).hexdigest()
        )

    @property
    def is_expired(self):
        return timezone.now() >= self.expires_at

    def __str__(self):
        return f"{self.user_id} - {self.purpose}"
