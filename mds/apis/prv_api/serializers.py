import json
from typing import List, Dict

from rest_framework import serializers

from mds import enums
from mds import models
from mds.apis import utils


class ProviderSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(
        required=True, help_text="Unique provider identifier (UUID)"
    )
    name = serializers.CharField(help_text="Name of the Provider")
    logo_b64 = serializers.CharField(
        required=False, help_text="Logo of provider base64 encoded"
    )

    class Meta:
        model = models.Provider
        fields = (
            "id",
            "name",
            "logo_b64",
            "base_api_url",
            "device_category",
            "api_authentication",
            "api_configuration",
            "agency_api_authentication",
        )


class PolygonRequestSerializer(serializers.ModelSerializer):
    """What we expect for a geographic polygon.
    """

    label = serializers.CharField(help_text="Name of the polygon")
    geom = utils.PolygonSerializer(help_text="GeoJSON Polygon")
    areas = serializers.PrimaryKeyRelatedField(many=True, queryset=models.Area.objects)

    class Meta:
        fields = ("geom", "label", "areas")
        model = models.Polygon

    def create(self, validated_data):
        instance = self.Meta.model(
            label=validated_data["label"], geom=json.dumps(validated_data["geom"])
        )
        instance.save()
        return instance

    def update(self, instance, validated_data):
        if validated_data.get("label"):
            instance.label = validated_data["label"]
        if validated_data.get("geom"):
            instance.geom = json.dumps(validated_data["geom"])
        if validated_data.get("areas"):
            areas = validated_data.pop("areas", [])
            instance.areas.set(areas)
        instance.save()
        return instance


class PolygonResponseSerializer(serializers.Serializer):
    """A representation of a geographic polygon.
    """

    id = serializers.UUIDField(help_text="Unique Polygon identifier (UUID)")
    label = serializers.CharField(help_text="Name of the polygon")
    geom = utils.PolygonSerializer(help_text="GeoJSON Polygon")
    areas = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        fields = ("id", "label", "geom", "areas")


class PolygonsImportRequestSerializer(serializers.Serializer):

    polygons = PolygonRequestSerializer(many=True)

    class Meta:
        fields = "polygons"


class AreaRequestSerializer(serializers.ModelSerializer):
    """A service area, composed of a group of Polygons.
    """

    label = serializers.CharField(help_text="Name of the Area")
    polygons = serializers.PrimaryKeyRelatedField(
        many=True, queryset=models.Polygon.objects
    )
    color = serializers.CharField(required=False, help_text="Color of the Area")

    class Meta:
        fields = ("label", "polygons", "color")
        model = models.Area

    def create(self, validated_data):
        instance = self.Meta.model(
            label=validated_data["label"], color=validated_data["color"]
        )
        instance.save()
        polygons = validated_data.get("polygons", [])
        instance.polygons.set(polygons)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        if validated_data.get("label"):
            instance.label = validated_data["label"]
        if validated_data.get("color"):
            instance.color = validated_data["color"]
        if "polygons" in validated_data:
            polygons = validated_data.get("polygons", [])
            instance.polygons.set(polygons)
        instance.save()
        return instance


class AreaResponseSerializer(serializers.Serializer):
    """A service area, composed of a group of Polygons.
    """

    id = serializers.UUIDField(help_text="Unique Area identifier (UUID)")
    label = serializers.CharField(help_text="Name of the Area")
    polygons = PolygonResponseSerializer(many=True)
    color = serializers.CharField(help_text="Color of the Area")

    class Meta:
        fields = ("id", "label", "polygons", "color")


class DeviceSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(help_text="Unique device identifier (UUID)")
    model = serializers.CharField(required=False, help_text="Vehicle model")
    identification_number = serializers.CharField(
        help_text="VIN (Vehicle Identification Number)"
    )
    category = serializers.ChoiceField(
        enums.choices(enums.DEVICE_CATEGORY), help_text="Device type"
    )
    propulsion = serializers.ListField(
        child=serializers.ChoiceField(enums.choices(enums.DEVICE_PROPULSION)),
        help_text="Propulsion type(s)",
    )
    provider_id = serializers.UUIDField(
        source="provider.id", help_text="ID of the service provider of the device"
    )
    provider_name = serializers.CharField(
        source="provider.name", help_text="Name of the service provider of the device"
    )
    registration_date = serializers.DateTimeField(help_text="Device registration date")
    last_telemetry_date = serializers.DateTimeField(
        source="dn_gps_timestamp", help_text="Latest GPS timestamp", allow_null=True
    )
    position = utils.PointSerializer(
        source="dn_gps_point", help_text="Latest GPS position"
    )
    status = serializers.ChoiceField(
        enums.choices(enums.DEVICE_STATUS),
        source="dn_status",
        help_text="Latest status",
        allow_null=True,
    )
    battery = serializers.FloatField(
        source="dn_battery_pct", help_text="Percentage between 0 and 1", allow_null=True
    )

    class Meta:
        model = models.Device
        fields = (
            "id",
            "provider_id",
            "provider_name",
            "model",
            "identification_number",
            "category",
            "propulsion",
            "status",
            "position",
            "registration_date",
            "last_telemetry_date",
            "battery",
        )


class RetrieveDeviceSerializer(DeviceSerializer):
    areas = serializers.SerializerMethodField()
    provider_logo = serializers.CharField(
        source="provider.logo_b64",
        help_text="logo in base 64 of the service provider of the device",
    )

    def get_areas(self, obj) -> List[Dict[str, str]]:
        if not obj.dn_gps_point:
            return []
        areas = (
            models.Area.objects.filter(polygons__geom__contains=obj.dn_gps_point)
            .order_by("label", "id")
            .distinct("label", "id")
        )
        return list(areas.values("id", "label"))

    class Meta:
        model = models.Device
        fields = DeviceSerializer.Meta.fields + ("areas", "provider_logo")
