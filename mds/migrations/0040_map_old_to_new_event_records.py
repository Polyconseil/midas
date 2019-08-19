# Generated by Django 2.1.11 on 2019-08-16 14:27

import datetime

from django.db import migrations, transaction
from django.db.models import Q

from mds.provider_mapping import (
    OLD_PROVIDER_REASON_TO_AGENCY_EVENT,
    OLD_TO_NEW_AGENCY_EVENT,
    PROVIDER_REASON_TO_AGENCY_EVENT,
)


def full_batch_apply(
    function, qs, collation=lambda a, b: a and b, initial_value=None, **kwargs
):
    batch_size = 1000
    try:
        first_pk = qs.order_by("pk").values_list("pk", flat=True)[0]
    except IndexError:
        return initial_value
    last_pk = qs.order_by("-pk").values_list("pk", flat=True)[0]
    start = max(1, first_pk)

    for i in range(start, last_pk + 1, batch_size):
        queryset = qs.filter(pk__gte=i, pk__lt=min(last_pk + 1, i + batch_size))
        try:
            with transaction.atomic():
                initial_value = collation(initial_value, function(queryset, **kwargs))
        except Exception:
            raise

    return initial_value


def fill_event_type_and_reason(apps, schema_editor):
    EventRecord = apps.get_model("mds", "EventRecord")

    for agency_event in OLD_PROVIDER_REASON_TO_AGENCY_EVENT.values():
        if agency_event in [x[0] for x in PROVIDER_REASON_TO_AGENCY_EVENT.values()]:
            # We do not want to apply the migration for the events
            # that are in both mappings (service_end, service_start, trip_end and trip_start)
            continue

        event = (agency_event,)
        new_agency_event = OLD_TO_NEW_AGENCY_EVENT.get(event, event)
        event_type, event_type_reason = (
            new_agency_event
            if len(new_agency_event) == 2
            else new_agency_event + (None,)
        )

        qs = EventRecord.objects.filter(Q(event_type=agency_event))

        def fill(qs):
            if event_type_reason:
                qs.update(event_type=event_type, event_type_reason=event_type_reason)
            else:
                qs.update(event_type=event_type)

        full_batch_apply(fill, qs)


def reverse_fill_event_type_and_reason(apps, schema_editor):
    EventRecord = apps.get_model("mds", "EventRecord")

    for agency_event in PROVIDER_REASON_TO_AGENCY_EVENT.values():
        if agency_event in [
            (event_type,) for event_type in OLD_PROVIDER_REASON_TO_AGENCY_EVENT.values()
        ]:
            # We do not want to apply the reverse migration to the events
            # that are in both mappings (service_end, service_start, trip_end and trip_start)
            continue

        old_event = (
            [
                old_event
                for old_event, new_event in OLD_TO_NEW_AGENCY_EVENT.items()
                if new_event == agency_event
            ]
            + [agency_event]  # if the event is not in the mapping
        )[0][0]

        event_type, event_type_reason = (
            agency_event if len(agency_event) == 2 else agency_event + (None,)
        )

        if event_type_reason:
            qs = EventRecord.objects.filter(
                Q(event_type=event_type) & Q(event_type_reason=event_type_reason)
            )
        else:
            qs = EventRecord.objects.filter(
                Q(event_type=event_type) & Q(event_type_reason__isnull=True)
            )

        def fill(qs):
            qs.update(event_type=old_event, event_type_reason=None)

        full_batch_apply(fill, qs)


class Migration(migrations.Migration):
    atomic = False
    deploy_phase = "0039_eventrecord_event_type_reason"

    dependencies = [("mds", "0039_eventrecord_event_type_reason")]

    operations = [
        migrations.RunPython(
            fill_event_type_and_reason, reverse_fill_event_type_and_reason
        )
    ]
