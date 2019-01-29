from rest_framework import routers
from django.conf.urls import url, include
from django.urls import path

from . import providers
from . import service_areas
from . import vehicles
from . import authent

def get_prv_router():
    """Generates a fresh router.

    Enables to register new routes even after .urls has
    been called on the router.
    """
    prv_router = routers.DefaultRouter()
    prv_router.register(r"providers", providers.ProviderViewSet)
    prv_router.register(r"service_areas", service_areas.AreaViewSet)
    prv_router.register(r"polygons", service_areas.PolygonViewSet)
    prv_router.register(r"vehicles", vehicles.DeviceViewSet, basename="device")
    return prv_router

app_name = "mds_prv_api"

urlpatterns = [
    path("authent", include(authent.urls))
]
urlpatterns += get_prv_router().urls