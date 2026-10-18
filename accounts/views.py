import secrets
from datetime import timedelta

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_http_methods

from .forms import RegisterForm
from .models import EmailOTP, User


OTP_SESSION_KEY = "pending_email_otp_id"
OTP_USER_SESSION_KEY = "pending_email_otp_user_id"
OTP_PURPOSE_SESSION_KEY = "pending_email_otp_purpose"

OTP_EXPIRY_MINUTES = 10
OTP_RESEND_SECONDS = 60
OTP_MAX_ATTEMPTS = 5


def send_otp(user, purpose):
    """Create and email a short-lived, six-digit verification code."""
    latest = EmailOTP.objects.filter(
        user=user,
        purpose=purpose,
    ).first()

    if latest and latest.used_at is None:
        elapsed = (timezone.now() - latest.created_at).total_seconds()
        if elapsed < OTP_RESEND_SECONDS:
            return False, "Please wait before requesting another code."

    code = f"{secrets.randbelow(1_000_000):06d}"

    otp = EmailOTP(
        user=user,
        purpose=purpose,
        expires_at=timezone.now() + timedelta(minutes=OTP_EXPIRY_MINUTES),
    )
    otp.set_code(code)
    otp.save()

    try:
        send_mail(
            subject="Your CountyConnect verification code",
            message=(
                f"Hello {user.username},\n\n"
                f"Your CountyConnect verification code is: {code}\n\n"
                f"This code expires in {OTP_EXPIRY_MINUTES} minutes. "
                "Do not share it with anyone.\n\n"
                "If you did not request this code, you can ignore this email."
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )
    except Exception:
        otp.delete()
        return False, "We could not send your email. Please try again later."

    return True, "Verification code sent to your email."


def set_pending_otp(request, user, purpose):
    request.session[OTP_USER_SESSION_KEY] = user.pk
    request.session[OTP_PURPOSE_SESSION_KEY] = purpose


@never_cache
@require_http_methods(["GET", "POST"])
def register(request):
    if request.user.is_authenticated:
        return redirect("services:my_requests")

    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            set_pending_otp(request, user, EmailOTP.REGISTRATION)

            success, detail = send_otp(user, EmailOTP.REGISTRATION)
            if success:
                latest = EmailOTP.objects.filter(
                    user=user,
                    purpose=EmailOTP.REGISTRATION,
                ).first()
                request.session[OTP_SESSION_KEY] = latest.pk
                messages.success(request, detail)
                return redirect("accounts:verify_email")

            messages.error(request, detail)
            return redirect("accounts:resend_otp")
    else:
        form = RegisterForm()

    return render(request, "accounts/register.html", {"form": form})


@never_cache
@require_http_methods(["GET", "POST"])
def login_view(request):
    if request.user.is_authenticated:
        return redirect("services:my_requests")

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()

            set_pending_otp(request, user, EmailOTP.LOGIN)

            success, detail = send_otp(user, EmailOTP.LOGIN)
            if success:
                latest = EmailOTP.objects.filter(
                    user=user,
                    purpose=EmailOTP.LOGIN,
                ).first()
                request.session[OTP_SESSION_KEY] = latest.pk
                messages.success(request, detail)
                return redirect("accounts:verify_login")

            messages.error(request, detail)
    else:
        form = AuthenticationForm(request)

    return render(request, "accounts/login.html", {"form": form})


@never_cache
@require_http_methods(["GET", "POST"])
def verify_email(request):
    return verify_otp(request, EmailOTP.REGISTRATION)


@never_cache
@require_http_methods(["GET", "POST"])
def verify_login(request):
    return verify_otp(request, EmailOTP.LOGIN)


def verify_otp(request, expected_purpose):
    otp_id = request.session.get(OTP_SESSION_KEY)
    user_id = request.session.get(OTP_USER_SESSION_KEY)
    purpose = request.session.get(OTP_PURPOSE_SESSION_KEY)

    if not otp_id or not user_id or purpose != expected_purpose:
        messages.error(request, "Please start the verification process again.")
        return redirect("accounts:login")

    otp = EmailOTP.objects.filter(
        pk=otp_id,
        user_id=user_id,
        purpose=expected_purpose,
        used_at__isnull=True,
    ).first()

    user = User.objects.filter(pk=user_id).first()

    if not otp or not user:
        messages.error(request, "This verification request is no longer valid.")
        return redirect("accounts:login")

    if request.method == "POST":
        code = request.POST.get("code", "").strip()

        if otp.is_expired:
            messages.error(request, "Your code has expired. Request a new one.")
        elif otp.attempts >= OTP_MAX_ATTEMPTS:
            messages.error(request, "Too many incorrect attempts. Request a new code.")
        elif len(code) != 6 or not code.isdigit() or not otp.check_code(code):
            otp.attempts += 1
            otp.save(update_fields=["attempts"])
            messages.error(request, "The code is incorrect. Please try again.")
        else:
            otp.used_at = timezone.now()
            otp.save(update_fields=["used_at"])

            if expected_purpose == EmailOTP.REGISTRATION:
                user.is_active = True
                user.save(update_fields=["is_active"])

            request.session.pop(OTP_SESSION_KEY, None)
            request.session.pop(OTP_USER_SESSION_KEY, None)
            request.session.pop(OTP_PURPOSE_SESSION_KEY, None)

            auth_login(request, user)
            messages.success(request, "Your email has been verified successfully.")
            return redirect("services:my_requests")

    return render(
        request,
        "accounts/verify_otp.html",
        {
            "purpose": expected_purpose,
            "email": user.email,
        },
    )


@never_cache
@require_http_methods(["GET", "POST"])
def resend_otp(request):
    user_id = request.session.get(OTP_USER_SESSION_KEY)
    purpose = request.session.get(OTP_PURPOSE_SESSION_KEY)

    if not user_id or purpose not in (
        EmailOTP.REGISTRATION,
        EmailOTP.LOGIN,
    ):
        messages.error(request, "Please start again to request a verification code.")
        return redirect("accounts:login")

    user = User.objects.filter(pk=user_id).first()

    if not user:
        messages.error(request, "Account not found.")
        return redirect("accounts:register")

    success, detail = send_otp(user, purpose)

    if success:
        latest = EmailOTP.objects.filter(
            user=user,
            purpose=purpose,
        ).first()
        request.session[OTP_SESSION_KEY] = latest.pk
        messages.success(request, detail)
    else:
        messages.error(request, detail)

    if purpose == EmailOTP.REGISTRATION:
        return redirect("accounts:verify_email")

    return redirect("accounts:verify_login")
