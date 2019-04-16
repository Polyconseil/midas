import random

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from django.db import IntegrityError

from mds import models
from mds.access_control.permissions import require_scopes
from mds.access_control.scopes import SCOPE_PRV_API
from mds.apis import utils

from rest_framework import filters

from . import serializers


class PolygonViewSet(utils.MultiSerializerViewSetMixin, viewsets.ModelViewSet):
    permission_classes = (require_scopes(SCOPE_PRV_API),)
    queryset = models.Polygon.objects.prefetch_related("areas").all()
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ("label",)
    ordering = "label"
    lookup_field = "id"
    serializer_class = serializers.PolygonResponseSerializer
    serializers_mapping = {
        "list": {"response": serializers.PolygonResponseSerializer},
        "retrieve": {"response": serializers.PolygonResponseSerializer},
        "create": {
            "request": serializers.PolygonRequestSerializer,
            "response": utils.EmptyResponseSerializer,
        },
        "update": {
            "request": serializers.PolygonRequestSerializer,
            "response": utils.EmptyResponseSerializer,
        },
        "import_polygons": {
            "request": serializers.PolygonsImportRequestSerializer,
            "response": utils.EmptyResponseSerializer,
        },
    }

    def create(self, *args, **kwargs):
        return super()._create(*args, **kwargs)

    def update(self, *args, **kwargs):
        return super()._update(*args, **kwargs)

    @action(methods=["post"], url_path="import", detail=False)
    def import_polygons(self, request, pk=None):
        polygons = request.data.get("polygons", None)

        if not isinstance(polygons, list):
            return Response(status=400)

        try:
            polygons_to_create = []
            for polygon in polygons:
                geom = polygon.get("geom", None)
                if geom and geom["type"] == "Polygon":

                    areas = []
                    for area_label in polygon.get("areas", []):
                        defaults = {"color": "#%06x" % random.randint(0, 0xFFFFFF)}
                        # Create new Area if doesn't exist (based on label)
                        area = models.Area.objects.get_or_create(
                            label=area_label, defaults=defaults
                        )[0]
                        areas.append(area)
                    poly = models.Polygon(
                        label=polygon.get("label", ""), geom=str(geom)
                    )
                    poly.areas.set([a.id for a in areas])
                    polygons_to_create.append(poly)
            models.Polygon.objects.bulk_create(polygons_to_create)
        except IntegrityError as ex:
            return Response(exception=ex, status=500)

        return Response({"message": "ok"})


class AreaViewSet(utils.MultiSerializerViewSetMixin, viewsets.ModelViewSet):
    permission_classes = (require_scopes(SCOPE_PRV_API),)
    queryset = models.Area.objects.prefetch_related("polygons").all()
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ("label",)
    ordering = "label"
    lookup_field = "id"
    serializer_class = serializers.AreaResponseSerializer
    serializers_mapping = {
        "list": {"response": serializers.AreaResponseSerializer},
        "retrieve": {"response": serializers.AreaResponseSerializer},
        "create": {
            "request": serializers.AreaRequestSerializer,
            "response": utils.EmptyResponseSerializer,
        },
        "update": {
            "request": serializers.AreaRequestSerializer,
            "response": utils.EmptyResponseSerializer,
        },
    }

    def create(self, *args, **kwargs):
        return super()._create(*args, **kwargs)

    def update(self, *args, **kwargs):
        return super()._update(*args, **kwargs)
