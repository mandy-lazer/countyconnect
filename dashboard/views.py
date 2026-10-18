import csv

from django.contrib.auth.decorators import user_passes_test
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render

from services.models import ServiceRequest


def staff_only(user):
    return user.is_authenticated and user.is_staff


@user_passes_test(staff_only, login_url='accounts:login')
def index(request):
    base = ServiceRequest.objects
    stats = {
        'total':       base.count(),
        'pending':     base.filter(status='pending').count(),
        'in_progress': base.filter(status='in_progress').count(),
        'resolved':    base.filter(status='resolved').count(),
        'rejected':    base.filter(status='rejected').count(),
    }
    by_category = base.values('category').annotate(count=Count('id')).order_by('-count')
    by_status   = base.values('status').annotate(count=Count('id'))
    recent      = base.order_by('-created_at')[:8]
    return render(request, 'dashboard/index.html', {
        'stats': stats,
        'by_category': list(by_category),
        'by_status': list(by_status),
        'recent': recent,
    })


@user_passes_test(staff_only, login_url='accounts:login')
def export_csv(request):
    resp = HttpResponse(content_type='text/csv')
    resp['Content-Disposition'] = 'attachment; filename="requests.csv"'
    writer = csv.writer(resp)
    writer.writerow(['Reference', 'Category', 'Location', 'Status', 'Priority', 'Citizen', 'Created'])
    for r in ServiceRequest.objects.all():
        writer.writerow([
            r.reference, r.get_category_display(), r.location,
            r.get_status_display(), r.get_priority_display(),
            r.citizen.username, r.created_at.isoformat(),
        ])
    return resp
