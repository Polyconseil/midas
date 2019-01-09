import collections
import json
import os.path
import warnings

import yaml
from django.db import connection
from django.db.models import OuterRef, Subquery, Prefetch
from django.shortcuts import render
from django_filters import rest_framework as filters
from rest_framework import exceptions
from rest_framework import serializers as drf_serializers
from rest_framework import viewsets
from rest_framework.compat import coreapi, coreschema
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.schemas import inspectors
from rest_framework.pagination import LimitOffsetPagination

from mds.access_control.permissions import require_scopes
from mds.access_control.scopes import SCOPE_VEHICLE
from . import models
from . import serializers
from . import enums


class MultiSerializerViewSet(viewsets.GenericViewSet):
    serializers_map = {}

    def get_serializer_class(self):
        return (
            self.serializers_map.get(self.action, None)
            or super().get_serializer_class()
        )


class CustomViewSchema(inspectors.AutoSchema):
    """
    Overrides `get_serializer_fields()`
    to accommodate our :class:`MultiSerializerViewSet`
    """

    def get_serializer_fields(self, path, method):
        view = self.view

        # set view action
        method = method.lower()
        if method == "options":
            view.action = "metadata"
        else:
            view.action = view.action_map.get(method)

        if method not in ("put", "patch", "post"):
            return []

        if not hasattr(view, "get_serializer"):
            return []

        try:
            serializer = view.get_serializer()
        except exceptions.APIException:
            serializer = None
            warnings.warn(
                "{}.get_serializer() raised an exception during "
                "schema generation. Serializer fields will not be "
                "generated for {} {}.".format(
                    view.__class__.__name__, method.upper(), path
                )
            )

        if isinstance(serializer, drf_serializers.ListSerializer):
            return [
                coreapi.Field(
                    name="data",
                    location="body",
                    required=True,
                    schema=coreschema.Array(),
                )
            ]

        if not isinstance(serializer, drf_serializers.Serializer):
            return []

        return [
            coreapi.Field(
                name=field.field_name,
                location="body",
                required=field.required and method != "patch",
                schema=inspectors.field_to_schema(field),
            )
            for field in serializer.fields.values()
            if not (field.read_only or isinstance(field, drf_serializers.HiddenField))
        ]


class UpdateOnlyModelMixin(object):
    """
    Update a model instance.
    """

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()


class DeviceLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 500


class DeviceFilter(filters.FilterSet):
    id = filters.CharFilter(lookup_expr="icontains")
    category = filters.MultipleChoiceFilter(choices=enums.DEVICE_CATEGORY_CHOICES)
    provider = filters.UUIDFilter()
    status = filters.MultipleChoiceFilter(
        "telemetries__status", choices=enums.DEVICE_STATUS_CHOICES
    )
    registrationDateFrom = filters.IsoDateTimeFilter(
        "registration_date", lookup_expr="gte"
    )
    registrationDateTo = filters.IsoDateTimeFilter(
        "registration_date", lookup_expr="lte"
    )

    class Meta:
        model = models.Device
        fields = [
            "id",
            "category",
            "provider",
            "status",
            "registrationDateFrom",
            "registrationDateTo",
        ]


class DeviceViewSet(
    viewsets.ModelViewSet, UpdateOnlyModelMixin, MultiSerializerViewSet
):
    def get_queryset(self):
        queryset = models.Device.objects

        user = self.request.user
        provider_id = getattr(self.request.user, "provider_id", None)
        if provider_id:
            queryset = queryset.filter(provider_id=user.provider_id)

        return queryset.prefetch_related(
            Prefetch(
                "telemetries",
                queryset=models.Telemetry.objects.filter(
                    id__in=Subquery(
                        models.Telemetry.objects.filter(device_id=OuterRef("device_id"))
                        .order_by("-timestamp")
                        .values_list("id", flat=True)[:1]
                    )
                ),
                to_attr="_latest_telemetry",
            )
        ).select_related("provider")

    permission_classes = (require_scopes(SCOPE_VEHICLE),)
    lookup_field = "id"
    serializers_map = {
        "list": serializers.Device,
        "retrieve": serializers.Device,
        "create": serializers.DeviceRegister,
        "update": serializers.DeviceRegister,
        "patch": serializers.DeviceRegister,
    }
    serializer_class = serializers.Device
    schema = CustomViewSchema()
    pagination_class = DeviceLimitOffsetPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = DeviceFilter

    @action(detail=False)
    def aggregations(self, request):
        query = """
            WITH filtered AS (
                SELECT DISTINCT ON ({device_table}.id) *
                FROM {device_table} JOIN {telemetry_table} ON {telemetry_table}.device_id = {device_table}.id
                {where_clause} ORDER BY {device_table}.id, {telemetry_table}.timestamp
            )
            SELECT 'provider' AS facet, provider_id::text AS value, count(*) AS count FROM filtered GROUP BY provider_id
            UNION
            SELECT 'category' AS facet, category AS value, count(*) AS count FROM filtered GROUP BY category
            UNION
            SELECT 'status' AS facet, status AS value, count(*) AS count FROM filtered GROUP BY status
            ORDER BY facet, value;
        """  # noqa
        queryset = self.filter_queryset(self.get_queryset())
        compiler = queryset.query.get_compiler(connection=connection)
        where_clause, where_args = compiler.compile(queryset.query.where)
        with connection.cursor() as cursor:
            where_clause = ("WHERE %s" % where_clause) if where_clause else ""
            cursor.execute(
                query.format(
                    where_clause=where_clause,
                    device_table=models.Device._meta.db_table,
                    telemetry_table=models.Telemetry._meta.db_table,
                ),
                where_args,
            )
            data = cursor.fetchall()
        result = {
            "aggregations": {
                "category": {cat: 0 for cat, _trans in enums.DEVICE_CATEGORY_CHOICES},
                "provider": collections.defaultdict(int),
                "status": {stat: 0 for stat, _trans in enums.DEVICE_STATUS_CHOICES},
            }
        }
        for facet, value, count in data:
            result["aggregations"][facet][value] += count
        return Response(result)


class AreaViewSet(viewsets.ModelViewSet):
    queryset = models.Area.objects.all()
    lookup_field = "id"
    serializer_class = serializers.AreaSerializer


class ProviderViewSet(viewsets.ModelViewSet):
    queryset = models.Provider.objects.all()
    lookup_field = "id"
    serializer_class = serializers.ProviderSerializer


def swagger(request):
    oas_file_path = os.path.join(os.path.dirname(__file__), "oas.yml")
    spec = json.dumps(yaml.load(open(oas_file_path)))
    return render(request, template_name="swagger.html", context={"data": spec})
