from django.contrib import admin
from .models import Vehicle, ServiceRecord


class ServiceRecordInline(admin.TabularInline):
    model = ServiceRecord
    extra = 0


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('name', 'number', 'vehicle_type', 'user')
    list_filter = ('vehicle_type',)
    search_fields = ('name', 'number', 'user__username')
    inlines = [ServiceRecordInline]


@admin.register(ServiceRecord)
class ServiceRecordAdmin(admin.ModelAdmin):
    list_display = ('vehicle', 'service_date', 'km_reading', 'cost')
    list_filter = ('service_date',)