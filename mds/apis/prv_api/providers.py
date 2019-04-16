from rest_framework import viewsets

from mds import models
from mds.access_control.permissions import require_scopes
from mds.access_control.scopes import SCOPE_PRV_API

from .serializers import ProviderSerializer


class ProviderViewSet(viewsets.ModelViewSet):
    permission_classes = (require_scopes(SCOPE_PRV_API),)
    queryset = models.Provider.objects.all()
    lookup_field = "id"
    serializer_class = ProviderSerializer
