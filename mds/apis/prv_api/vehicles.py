from django_filters import rest_framework as filters
from rest_framework import viewsets

from mds import enums, models
from mds.access_control.permissions import require_scopes
from mds.access_control.scopes import SCOPE_PRV_API
from mds.apis import utils

from . import serializers


class DeviceFilter(filters.FilterSet):
    id = filters.CharFilter(lookup_expr="icontains")
    category = utils.ChoicesInFilter(choices=enums.choices(enums.DEVICE_CATEGORY))
    provider = utils.UUIDInFilter()
    status = utils.ChoicesInFilter(
        "dn_status", choices=enums.choices(enums.DEVICE_STATUS)
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


class DeviceViewSet(utils.MultiSerializerViewSetMixin, viewsets.ReadOnlyModelViewSet):
    permission_classes = (require_scopes(SCOPE_PRV_API),)
    lookup_field = "id"
    serializer_class = serializers.DeviceSerializer
    pagination_class = utils.LimitOffsetPagination
    filter_backends = (filters.DjangoFilterBackend,)

    filterset_class = DeviceFilter
    queryset = models.Device.objects.select_related("provider").all()
    serializers_mapping = {
        "list": {"response": serializers.DeviceSerializer},
        "retrieve": {"response": serializers.RetrieveDeviceSerializer},
    }
