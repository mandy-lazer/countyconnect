from django.contrib import admin

from .models import ServiceRequest, StatusUpdate


@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display  = ('reference', 'category', 'citizen', 'status', 'priority', 'created_at')
    list_filter   = ('status', 'category', 'priority')
    search_fields = ('reference', 'location', 'citizen__username')


admin.site.register(StatusUpdate)
