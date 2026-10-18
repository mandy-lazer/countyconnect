import uuid

from django.conf import settings
from django.db import models
from django.urls import reverse


class Category(models.TextChoices):
    STREETLIGHT = 'streetlight', 'Broken Streetlight'
    WATER       = 'water',       'Water Issue'
    GARBAGE     = 'garbage',     'Garbage Collection'
    ROADS       = 'roads',       'Roads & Drainage'
    OTHER       = 'other',       'Other'


class Priority(models.TextChoices):
    LOW    = 'low',    'Low'
    MEDIUM = 'medium', 'Medium'
    HIGH   = 'high',   'High'


class ServiceRequest(models.Model):
    class Status(models.TextChoices):
        PENDING     = 'pending',     'Pending'
        IN_PROGRESS = 'in_progress', 'In Progress'
        RESOLVED    = 'resolved',    'Resolved'
        REJECTED    = 'rejected',    'Rejected'

    reference   = models.CharField(max_length=12, unique=True, editable=False)
    citizen     = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='requests',
    )
    category    = models.CharField(max_length=20, choices=Category.choices)
    location    = models.CharField(max_length=200)
    description = models.TextField()
    image       = models.ImageField(upload_to='requests/%Y/%m/', blank=True, null=True)
    priority    = models.CharField(max_length=10, choices=Priority.choices, default=Priority.MEDIUM)
    status      = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)

    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='assigned_requests',
        limit_choices_to={'is_staff': True},
    )
    resolution_notes = models.TextField(blank=True)
    resolved_at      = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.reference:
            self.reference = f"CSR-{uuid.uuid4().hex[:6].upper()}"
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('services:detail', kwargs={'reference': self.reference})

    def __str__(self):
        return f"{self.reference} — {self.get_category_display()}"


class StatusUpdate(models.Model):
    """Audit trail for every status change."""
    request    = models.ForeignKey(
        ServiceRequest, on_delete=models.CASCADE, related_name='updates',
    )
    old_status = models.CharField(max_length=20, choices=ServiceRequest.Status.choices, blank=True)
    new_status = models.CharField(max_length=20, choices=ServiceRequest.Status.choices)
    note       = models.TextField(blank=True)
    changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.request.reference}: {self.old_status or '∅'} → {self.new_status}"
