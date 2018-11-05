import json

from django.contrib.gis.geos import MultiPolygon
from django.contrib.gis.geos.geometry import GEOSGeometry
from rest_framework import serializers

from . import enums
from . import models


class GeometryField(serializers.Field):
    type_name = "GeometryField"

    def to_representation(self, value):
        if isinstance(value, dict) or value is None:
            return value
        return value.geojson

    def to_internal_value(self, value):
        if not value or isinstance(value, GEOSGeometry):
            return value
        if isinstance(value, dict):
            value = json.dumps(value)
        return GEOSGeometry(value)


class Device(serializers.Serializer):
    id = serializers.UUIDField()
    provider = serializers.UUIDField()
    identification_number = serializers.CharField()
    model = serializers.CharField()
    status = serializers.ChoiceField(enums.DEVICE_STATUS_CHOICES)
    position = GeometryField(required=False, allow_null=True)
    properties = serializers.JSONField(default=dict, required=False)


class DeviceRegister(serializers.Serializer):
    id = serializers.UUIDField()
    provider = serializers.UUIDField()
    identification_number = serializers.CharField()
    model = serializers.CharField()

    def create(self, data):
        return models.Device.objects.create(**data)


class DeviceTelemetry(serializers.Serializer):
    id = serializers.UUIDField()
    provider = serializers.UUIDField()
    status = serializers.ChoiceField(enums.DEVICE_STATUS_CHOICES)
    position = GeometryField(required=False, allow_null=True)
    properties = serializers.JSONField(default=dict, required=False)

    def update(self, instance, data):
        return models.Device.objects.filter(
            id=data.pop("id"), provider=data.pop("provider")
        ).update(**data)


class ServiceAreaSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    begin_date = serializers.DateTimeField()
    end_date = serializers.DateTimeField(required=False)
    # TODO are should be a Feature of MultiPolygon.
    # It is a single polygon for the moment
    # NOTE (lip): We could use a FeatureCollection of Polygons instead.
    polygon = GeometryField()

    def create(self, data):
        area = models.Area.objects.create(
            polygons=MultiPolygon([data["area"]["polygons"]])
        )
        return models.Service.objects.create(
            area=area,
            provider="bluela",
            begin_date=data["begin_date"],
            end_date=data.get("end_date"),
        )
