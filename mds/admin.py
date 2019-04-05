from django.contrib import admin
from . import models

from uuid import UUID


def is_uuid(uuid_string, version=4):
    try:
        uid = UUID(uuid_string, version=version)
        return uid.hex == uuid_string.replace("-", "")
    except ValueError:
        return False


@admin.register(models.Provider)
class ProviderAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    ordering = ["name"]


@admin.register(models.Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ["id", "provider", "identification_number", "category"]
    list_filter = ["provider", "model", "category"]
    search_fields = ["id", "identification_number"]


@admin.register(models.EventRecord)
class EventRecordAdmin(admin.ModelAdmin):
    list_display = ["timestamp", "provider", "device_id", "event_type"]
    list_filter = ["device__provider", "event_type"]
    list_select_related = ("device__provider",)
    search_fields = ["device__id", "device__identification_number"]

    def get_search_results(self, request, queryset, search_term):
        if not search_term:
            return super().get_search_results(request, queryset, search_term)
        custom_queryset = get_devices_queryset_search_results(self, search_term)
        return super().get_search_results(request, custom_queryset, search_term)

    def provider(self, obj):
        return obj.device.provider.name

    def device_id(self, obj):
        return obj.device.id


# to use when searching for devices in get_search_results as a relationship to self.model
def get_devices_queryset_search_results(self, search_term):
    custom_queryset = self.model.objects.select_related("device__provider")
    if is_uuid(search_term):
        return custom_queryset.filter(device_id=search_term)
    else:
        return custom_queryset.filter(device__identification_number=search_term)


@admin.register(models.Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ["id", "creation_date", "deletion_date", "label"]
    list_filter = ["creation_date", "deletion_date"]
    ordering = ["-creation_date"]


@admin.register(models.Polygon)
class PolygonAdmin(admin.ModelAdmin):
    list_display = ["id", "creation_date", "deletion_date", "label"]
    list_filter = ["creation_date", "deletion_date"]
    ordering = ["-creation_date"]
