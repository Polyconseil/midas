import datetime
import logging
import traceback
import urllib.parse

from django.contrib.gis import geos
from django.core import management
from django.db import transaction
from django.db.models.aggregates import Max

import requests
import pytz

from mds import models


NOT_PROVIDED = object()

logger = logging.getLogger(__name__)


class Command(management.BaseCommand):
    help = "Poll providers to fetch their latest data."

    def handle(self, *args, **options):
        for provider in models.Provider.objects.all():
            if not provider.base_api_url:
                self.stdout.write(
                    "Provider %s has no URL defined, skipping." % provider.name
                )
                continue

            self.stdout.write("Polling %s... " % provider.name, ending="")
            try:
                with transaction.atomic():
                    self.poll_status_changes(provider)
            except Exception:  # pylint: disable=broad-except
                logger.exception("Error in polling provider %s", provider.name)
                self.stderr.write("Polling failed!")
                self.stderr.write(traceback.format_exc())
                # Try the next provider anyway
                continue

            self.stdout.write("Success!")

    def poll_status_changes(self, provider):
        next_url = urllib.parse.urljoin(provider.base_api_url, "/status_changes")
        # Start where we left
        # (we wouldn't know if the provider recorded late telemetries after the last sync)
        max_timestamp = models.EventRecord.objects.filter(
            device__provider=provider
        ).aggregate(max_timestamp=Max("timestamp"))["max_timestamp"]
        if max_timestamp:
            next_url = "%s?%s" % (
                next_url,
                urllib.parse.urlencode(
                    {"start_time": int(max_timestamp.timestamp() * 1000)}
                ),
            )

        # Pagination
        while next_url:
            data = self.get_data(next_url)
            for status_change in data["data"]["status_changes"]:
                device, created = models.Device.objects.get_or_create(
                    pk=status_change["device_id"],
                    defaults={
                        "provider": provider,
                        "identification_number": status_change["vehicle_id"],
                        "category": status_change["vehicle_type"],
                        "propulsion": status_change["propulsion_type"],
                    },
                )
                if created:
                    self.stdout.write(
                        "Device %s was created." % status_change["device_id"]
                    )

                event_location = status_change["event_location"]
                assert event_location["geometry"]["type"] == "Point"

                # Filtering on start_time *should* be implemented
                # So consider timestamps as unique per device
                device.event_records.get_or_create(
                    timestamp=datetime.datetime.fromtimestamp(
                        status_change["event_time"] / 1000, pytz.utc
                    ),
                    defaults=dict(
                        source="pull",  # pulled by agency
                        point=geos.Point(event_location["geometry"]["coordinates"]),
                        # XXX Vocabulary mismatch between agency and provider
                        event_type=status_change["event_type_reason"],
                        properties={
                            "trip_id": None,  # XXX I receive a list
                            "telemetry": {
                                "timestamp": event_location["properties"]["timestamp"],
                                "gps": {
                                    "lng": event_location["geometry"]["coordinates"][0],
                                    "lat": event_location["geometry"]["coordinates"][1],
                                    # XXX altitude, etc.?
                                },
                            },
                        },
                    ),
                )

            next_url = data["links"].get("next", NOT_PROVIDED)
            if next_url is NOT_PROVIDED:
                self.stdout.write(
                    "Warning: provider %s doesn't provide a next URL, cannot batch."
                    % provider.name
                )
                # We'll poll the next page on the next round
                # Hoping that they *do* implement "start_time"...
                next_url = None

    def get_data(self, url):
        response = requests.get(url, timeout=30)  # TODO authentication
        response.raise_for_status()
        return response.json()
