from rest_framework import viewsets
from rest_framework import generics
from rest_framework import response
from rest_framework import status

from . import models
from . import serializers


class ViewSet(viewsets.ModelViewSet):
    serializers_map = {}

    def get_serializer_class(self):
        return (
            self.serializers_map.get(self.action, None)
            or super().get_serializer_class()
        )

    def get_object(self):
        lookups = getattr(self, "lookups", [])
        if not lookups:
            return super().get_object()

        queryset = self.filter_queryset(self.get_queryset())
        for lookup in lookups:
            assert lookup.url_kwarg in self.kwargs, (
                "Expected view %s to be called with a URL keyword argument "
                'named "%s". Fix your URL conf, or set the `.lookup_field` '
                "attribute on the view correctly."
                % (self.__class__.__name__, lookup.url_kwarg)
            )
        filter_kwargs = {
            lookup.field: self.kwargs[lookup.url_kwarg] for lookup in lookups
        }
        obj = generics.get_object_or_404(queryset, **filter_kwargs)
        self.check_object_permissions(self.request, obj)
        return obj

    def create(self, request, *args, **kwargs):
        data = {}
        data.update(request.data)
        data.update(kwargs)
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return response.Response(status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        data = {}
        data.update(request.data)
        data.update(kwargs)
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return response.Response()


class Lookup:
    def __init__(self, field=None, url_kwarg=None, regex="[^/.]+"):
        self.field = field or "pk"
        self.url_kwarg = url_kwarg or self.field
        self.regex = regex


class AreaViewSet(ViewSet):
    queryset = models.Area.objects.all()
    serializer_class = serializers.ServiceAreaSerializer
    lookups = [Lookup("provider"), Lookup("id")]


class DeviceViewSet(ViewSet):
    queryset = models.Device.objects.all()
    lookups = [Lookup("provider"), Lookup("id")]
    serializers_map = {
        "list": serializers.Device,
        "retrieve": serializers.Device,
        "create": serializers.DeviceRegister,
        "update": serializers.DeviceTelemetry,
    }
