"""
URL Configuration
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.urls import path
from rest_framework import routers

from . import views


class MultiLookupRouter(routers.DefaultRouter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    routes = [
        # List route.
        routers.Route(
            url=r"^{prefix}{trailing_slash}$",
            mapping={"get": "list"},
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
                "put": "create",
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

    def get_lookup_regex(self, viewset, lookup_prefix=""):
        lookups = getattr(viewset, "lookups", [])
        if not lookups:
            return super().get_lookup_regex(viewset, lookup_prefix)
        return "/".join(
            "(?P<{lookup_prefix}{lookup.url_kwarg}>{lookup.regex})".format(
                lookup=lookup, lookup_prefix=lookup_prefix
            )
            for lookup in lookups
        )


router = MultiLookupRouter()
router.register(r"service_area", views.AreaViewSet)
router.register(r"vehicle", views.DeviceViewSet)

urlpatterns = [url(r"^", include(router.urls)), path("admin/", admin.site.urls)]
