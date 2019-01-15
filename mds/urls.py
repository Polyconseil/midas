from django.conf.urls import include
from django.conf.urls import url
from django.contrib import admin
from django.http import HttpResponse
from django.urls import path
from rest_framework import routers, permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from . import views


class PutCreateRouter(routers.DefaultRouter):
    """DefaultRouter with a custom detail route mapping: PUT creates and POST updates.
    """

    routes = [
        # List route.
        routers.Route(
            url=r"^{prefix}{trailing_slash}$",
            mapping={"get": "list", "post": "create"},
            name="{basename}-list",
            detail=False,
            initkwargs={"suffix": "List"},
        ),
        # Dynamically generated list routes. Generated using
        # @action(detail=False) decorator on methods of the viewset.
        routers.DynamicRoute(
            url=r"^{prefix}/{url_path}{trailing_slash}$",
            name="{basename}-{url_name}",
            detail=False,
            initkwargs={},
        ),
        # Detail route.
        routers.Route(
            url=r"^{prefix}/{lookup}{trailing_slash}$",
            mapping={
                "get": "retrieve",
                "post": "update",
                "patch": "partial_update",
                "delete": "destroy",
            },
            name="{basename}-detail",
            detail=True,
            initkwargs={"suffix": "Instance"},
        ),
        # Dynamically generated detail routes. Generated using
        # @action(detail=True) decorator on methods of the viewset.
        routers.DynamicRoute(
            url=r"^{prefix}/{lookup}/{url_path}{trailing_slash}$",
            name="{basename}-{url_name}",
            detail=True,
            initkwargs={},
        ),
    ]


router = PutCreateRouter()
router.register(r"providers", views.ProviderViewSet)
# TODO use plural for ressources in URL to be MDS (and rest of the world) compliant
# TODO Separated /mds resources and /prv endpoints
router.register(r"service_area", views.AreaViewSet)
router.register(r"vehicle", views.DeviceViewSet, basename="device")


def ok_view(request):
    return HttpResponse("OK", status=200)


schema_view = get_schema_view(
    openapi.Info(title="Plato API", default_version="v1", description="Plato API"),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    url(r"^", include(router.urls)),
    url(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path("admin/", admin.site.urls),
    path("selftest/ping/", ok_view),
]
