import re

from django.urls import include, path, re_path

from rest_framework import permissions
from rest_framework import routers
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from . import geographies
from . import policies
from . import vehicles
from . import compliances


agency_router = routers.DefaultRouter()
agency_router.register(r"vehicles", vehicles.DeviceViewSet, basename="device")
agency_router.register(r"policies", policies.PolicyViewSet, basename="policy")
agency_router.register(
    r"compliance/snapshot", compliances.ComplianceViewSet, basename="compliance"
)

agency_router.register(
    r"geographies", geographies.GeographyViewSet, basename="geography"
)


def get_url_patterns(prefix):
    # the schema view needs the prefix to generate correct urls
    # => url_patterns cannot be hardcoded here
    prefix = re.split(r"[/]+$", prefix)[0]
    prefix = ("%s/" % prefix) if prefix else ""
    schema_view = get_schema_view(
        openapi.Info(
            title="LADOT agency API",
            default_version="v0.2",
            description="see "
            "https://github.com/CityOfLosAngeles/mobility-data-specification",
        ),
        patterns=[path(prefix, include(agency_router.urls))],
        public=True,
        permission_classes=(permissions.AllowAny,),
    )

    return agency_router.urls + [
        re_path(
            r"^swagger(?P<format>\.json|\.yaml)$",
            schema_view.without_ui(cache_timeout=0),
            name="schema-json",
        ),
        re_path(
            r"^swagger/$",
            schema_view.with_ui("swagger", cache_timeout=0),
            name="schema-swagger-ui",
        ),
    ]
