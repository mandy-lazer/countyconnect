
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import ServiceRequestForm
from .models import Category, ServiceRequest, StatusUpdate


@login_required
def submit_request(request):
    if request.method == 'POST':
        form = ServiceRequestForm(request.POST, request.FILES)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.citizen = request.user
            obj.save()

            StatusUpdate.objects.create(
                request=obj,
                old_status='',
                new_status=obj.status,
                note='Request submitted.',
                changed_by=request.user,
            )

            messages.success(
                request,
                f"Request submitted. Reference: {obj.reference}"
            )

            return redirect(
                'services:detail',
                reference=obj.reference
            )
    else:
        form = ServiceRequestForm()

    return render(
        request,
        'services/submit.html',
        {'form': form}
    )


@login_required
def my_requests(request):
    # Requests belonging to the logged-in citizen
    qs = ServiceRequest.objects.filter(citizen=request.user)

    # Calculate statistics before applying the status filter
    total_cases = qs.count()

    resolved_cases = qs.filter(
        status=ServiceRequest.Status.RESOLVED
    ).count()

    in_progress_cases = qs.filter(
        status=ServiceRequest.Status.IN_PROGRESS
    ).count()

    pending_cases = qs.filter(
        status=ServiceRequest.Status.PENDING
    ).count()

    # Optional status filter
    status = request.GET.get('status')

    if status in dict(ServiceRequest.Status.choices):
        qs = qs.filter(status=status)

    context = {
        'requests': qs,
        'filter': status,
        'total_cases': total_cases,
        'resolved_cases': resolved_cases,
        'in_progress_cases': in_progress_cases,
        'pending_cases': pending_cases,
    }

    return render(
        request,
        'services/my_requests.html',
        context
    )


@login_required
def detail(request, reference):
    req = get_object_or_404(
        ServiceRequest,
        reference=reference
    )

    # Citizens can only view their own requests.
    # Staff can view any request.
    if not request.user.is_staff and req.citizen != request.user:
        return redirect('services:my_requests')

    return render(
        request,
        'services/detail.html',
        {'req': req}
    )


def track(request):
    reference = request.GET.get('ref', '').strip().upper()

    req = None

    if reference:
        req = ServiceRequest.objects.filter(
            reference=reference
        ).first()

    return render(
        request,
        'services/track.html',
        {
            'req': req,
            'reference': reference,
        }
    )


def staff_only(user):
    return user.is_authenticated and user.is_staff


@user_passes_test(staff_only, login_url='accounts:login')
def manage_requests(request):
    qs = ServiceRequest.objects.all()

    status = request.GET.get('status')
    category = request.GET.get('category')

    # Filter by a valid status
    if status in dict(ServiceRequest.Status.choices):
        qs = qs.filter(status=status)

    # FIX: Category is a top-level model choice class.
    if category in dict(Category.choices):
        qs = qs.filter(category=category)

    context = {
        'requests': qs,
        'status': status,
        'category': category,
    }

    return render(
        request,
        'dashboard/manage.html',
        context
    )


@user_passes_test(staff_only, login_url='accounts:login')
def update_status(request, reference):
    req = get_object_or_404(
        ServiceRequest,
        reference=reference
    )

    if request.method == 'POST':
        new_status = request.POST.get('status')
        note = request.POST.get('note', '').strip()

        if new_status in dict(ServiceRequest.Status.choices):
            old_status = req.status
            req.status = new_status

            if new_status == ServiceRequest.Status.RESOLVED:
                req.resolved_at = timezone.now()
            else:
                req.resolved_at = None

            if note:
                req.resolution_notes = note

            if not req.assigned_to:
                req.assigned_to = request.user

            req.save()

            StatusUpdate.objects.create(
                request=req,
                old_status=old_status,
                new_status=new_status,
                note=note,
                changed_by=request.user,
            )

            messages.success(
                request,
                f"Status updated to {req.get_status_display()}."
            )
        else:
            messages.error(
                request,
                "Invalid status."
            )

    return redirect(
        'services:detail',
        reference=req.reference
    )