from mds.enums import (
    DEVICE_STATUS,
    EVENT_TYPE,
    EVENT_TYPE_REASON,
    PROVIDER_EVENT_TYPE_REASON,
)


# Mappings between Provider and Agency
#
# When we poll providers (with provider API) we cast the event reason
# with PROVIDER_REASON_TO_AGENCY_EVENT because enums don't match
# and we use Agency API nomenclature
# Then when we are ourselves polled we use AGENCY_EVENT_TO_PROVIDER_REASON
# and PROVIDER_EVENT_TYPE_REASON_TO_EVENT_TYPE to be compliant
# with Provider API nomenclature

# Converts a Provider event_type_reason to an Agency event_type
# and event_type_reason (when needed), order by key as in:
# https://github.com/CityOfLosAngeles/mobility-data-specification/tree/dev/provider
PROVIDER_REASON_TO_AGENCY_EVENT = {
    # available #
    PROVIDER_EVENT_TYPE_REASON.service_start.name: (EVENT_TYPE.service_start.name,),
    PROVIDER_EVENT_TYPE_REASON.user_drop_off.name: (EVENT_TYPE.trip_end.name,),
    PROVIDER_EVENT_TYPE_REASON.rebalance_drop_off.name: (
        EVENT_TYPE.provider_drop_off.name,
    ),
    # There is no equivalent on the agency side of maintenance_drop_off.
    # This is the closest
    PROVIDER_EVENT_TYPE_REASON.maintenance_drop_off.name: (
        EVENT_TYPE.provider_drop_off.name,
        EVENT_TYPE_REASON.maintenance.name,
    ),
    PROVIDER_EVENT_TYPE_REASON.agency_drop_off.name: (
        PROVIDER_EVENT_TYPE_REASON.agency_drop_off.name,
    ),
    # reserved #
    PROVIDER_EVENT_TYPE_REASON.user_pick_up.name: (EVENT_TYPE.trip_start.name,),
    # unavailable #
    PROVIDER_EVENT_TYPE_REASON.maintenance.name: (
        EVENT_TYPE.service_end.name,
        EVENT_TYPE_REASON.maintenance.name,
    ),
    PROVIDER_EVENT_TYPE_REASON.low_battery.name: (
        EVENT_TYPE.service_end.name,
        EVENT_TYPE_REASON.low_battery.name,
    ),
    # removed #
    PROVIDER_EVENT_TYPE_REASON.service_end.name: (EVENT_TYPE.service_end.name,),
    # There is no equivalent on the agency side of rebalance_pick_up.
    PROVIDER_EVENT_TYPE_REASON.rebalance_pick_up.name: (
        EVENT_TYPE.provider_pick_up.name,
        EVENT_TYPE_REASON.rebalance.name,
    ),
    PROVIDER_EVENT_TYPE_REASON.maintenance_pick_up.name: (
        EVENT_TYPE.provider_pick_up.name,
        EVENT_TYPE_REASON.maintenance.name,
    ),
    PROVIDER_EVENT_TYPE_REASON.agency_pick_up.name: (EVENT_TYPE.city_pick_up.name,),
}

OLD_PROVIDER_REASON_TO_AGENCY_EVENT = {
    "service_start": EVENT_TYPE.service_start.name,
    "user_drop_off": EVENT_TYPE.trip_end.name,
    "rebalance_drop_off": PROVIDER_EVENT_TYPE_REASON.rebalance_drop_off.name,
    "maintenance_drop_off": PROVIDER_EVENT_TYPE_REASON.maintenance_drop_off.name,
    "user_pick_up": EVENT_TYPE.trip_start.name,
    "maintenance": PROVIDER_EVENT_TYPE_REASON.maintenance.name,
    "low_battery": PROVIDER_EVENT_TYPE_REASON.low_battery.name,
    "service_end": EVENT_TYPE.service_end.name,
    "rebalance_pick_up": PROVIDER_EVENT_TYPE_REASON.rebalance_pick_up.name,
    "maintenance_pick_up": PROVIDER_EVENT_TYPE_REASON.maintenance_pick_up.name,
}


# Converts an Agency event to a Provider event_type_reason
# Try to stay consistent with
# https://github.com/CityOfLosAngeles/mds-core/blob/master/packages/mds-provider/utils.ts
AGENCY_EVENT_TO_PROVIDER_REASON = {
    (EVENT_TYPE.register.name,): PROVIDER_EVENT_TYPE_REASON.service_end.name,
    (EVENT_TYPE.service_start.name,): PROVIDER_EVENT_TYPE_REASON.service_start.name,
    (EVENT_TYPE.service_end.name,): PROVIDER_EVENT_TYPE_REASON.service_end.name,
    (
        EVENT_TYPE.service_end.name,
        EVENT_TYPE_REASON.low_battery.name,
    ): PROVIDER_EVENT_TYPE_REASON.low_battery.name,
    (
        EVENT_TYPE.service_end.name,
        EVENT_TYPE_REASON.maintenance.name,
    ): PROVIDER_EVENT_TYPE_REASON.maintenance.name,
    (
        EVENT_TYPE.service_end.name,
        EVENT_TYPE_REASON.compliance.name,
    ): PROVIDER_EVENT_TYPE_REASON.service_end.name,
    (
        EVENT_TYPE.service_end.name,
        EVENT_TYPE_REASON.off_hours.name,
    ): PROVIDER_EVENT_TYPE_REASON.service_end.name,
    (
        EVENT_TYPE.provider_drop_off.name,
    ): PROVIDER_EVENT_TYPE_REASON.rebalance_drop_off.name,
    # Not in the Agency spec but in the provider spec
    (
        EVENT_TYPE.provider_drop_off.name,
        EVENT_TYPE_REASON.maintenance.name,
    ): PROVIDER_EVENT_TYPE_REASON.maintenance_drop_off.name,
    (EVENT_TYPE.provider_pick_up.name,): PROVIDER_EVENT_TYPE_REASON.service_end.name,
    (
        EVENT_TYPE.provider_pick_up.name,
        EVENT_TYPE_REASON.rebalance.name,
    ): PROVIDER_EVENT_TYPE_REASON.rebalance_pick_up.name,
    (
        EVENT_TYPE.provider_pick_up.name,
        EVENT_TYPE_REASON.maintenance.name,
    ): PROVIDER_EVENT_TYPE_REASON.maintenance_pick_up.name,
    (
        EVENT_TYPE.provider_pick_up.name,
        EVENT_TYPE_REASON.charge.name,
    ): PROVIDER_EVENT_TYPE_REASON.maintenance_pick_up.name,
    (
        EVENT_TYPE.provider_pick_up.name,
        EVENT_TYPE_REASON.compliance.name,
    ): PROVIDER_EVENT_TYPE_REASON.service_end.name,
    # no city_pick_up in provider's spec
    (EVENT_TYPE.city_pick_up.name,): PROVIDER_EVENT_TYPE_REASON.agency_pick_up.name,
    (EVENT_TYPE.reserve.name,): PROVIDER_EVENT_TYPE_REASON.user_pick_up.name,
    (
        EVENT_TYPE.cancel_reservation.name,
    ): PROVIDER_EVENT_TYPE_REASON.user_drop_off.name,
    (EVENT_TYPE.trip_start.name,): PROVIDER_EVENT_TYPE_REASON.user_pick_up.name,
    (EVENT_TYPE.trip_enter.name,): PROVIDER_EVENT_TYPE_REASON.user_pick_up.name,
    (EVENT_TYPE.trip_leave.name,): PROVIDER_EVENT_TYPE_REASON.service_end.name,
    (EVENT_TYPE.trip_end.name,): PROVIDER_EVENT_TYPE_REASON.user_drop_off.name,
    (EVENT_TYPE.deregister.name,): PROVIDER_EVENT_TYPE_REASON.service_end.name,
    (
        EVENT_TYPE.deregister.name,
        EVENT_TYPE_REASON.missing.name,
    ): PROVIDER_EVENT_TYPE_REASON.service_end.name,
    (
        EVENT_TYPE.deregister.name,
        EVENT_TYPE_REASON.decommissioned.name,
    ): PROVIDER_EVENT_TYPE_REASON.service_end.name,
    # Not in the MDS agency spec: probably not used
    (
        PROVIDER_EVENT_TYPE_REASON.agency_drop_off.name,
    ): PROVIDER_EVENT_TYPE_REASON.agency_drop_off.name,  # not used
    (
        PROVIDER_EVENT_TYPE_REASON.agency_pick_up.name,
    ): PROVIDER_EVENT_TYPE_REASON.agency_pick_up.name,  # not used
    (
        EVENT_TYPE.battery_charged.name,
    ): PROVIDER_EVENT_TYPE_REASON.maintenance_drop_off.name,  # not used
}

OLD_AGENCY_EVENT_TO_PROVIDER_REASON = {
    EVENT_TYPE.service_start.name: "service_start",
    EVENT_TYPE.cancel_reservation.name: "user_drop_off",
    EVENT_TYPE.trip_end.name: "user_drop_off",
    PROVIDER_EVENT_TYPE_REASON.rebalance_drop_off.name: "rebalance_drop_off",
    PROVIDER_EVENT_TYPE_REASON.maintenance_drop_off.name: "maintenance_drop_off",
    EVENT_TYPE.battery_charged.name: "maintenance_drop_off",
    EVENT_TYPE.reserve.name: "user_pick_up",
    EVENT_TYPE.trip_start.name: "user_pick_up",
    EVENT_TYPE.trip_enter.name: "user_pick_up",
    EVENT_TYPE.trip_leave.name: "user_pick_up",  # This is on really bad...
    PROVIDER_EVENT_TYPE_REASON.low_battery.name: "low_battery",
    PROVIDER_EVENT_TYPE_REASON.maintenance.name: "maintenance",
    EVENT_TYPE.deregister.name: "service_end",
    EVENT_TYPE.service_end.name: "service_end",
    EVENT_TYPE.register.name: "service_end",
    PROVIDER_EVENT_TYPE_REASON.rebalance_pick_up.name: "rebalance_pick_up",
    PROVIDER_EVENT_TYPE_REASON.maintenance_pick_up.name: "maintenance_pick_up",
}

# Inside the Provider API, maps the event_type_reason to the corresponding event_type
# https://github.com/CityOfLosAngeles/mobility-data-specification/tree/dev/provider
PROVIDER_EVENT_TYPE_REASON_TO_EVENT_TYPE = {
    # available #
    PROVIDER_EVENT_TYPE_REASON.service_start.name: DEVICE_STATUS.available.name,
    PROVIDER_EVENT_TYPE_REASON.user_drop_off.name: DEVICE_STATUS.available.name,
    PROVIDER_EVENT_TYPE_REASON.rebalance_drop_off.name: DEVICE_STATUS.available.name,
    PROVIDER_EVENT_TYPE_REASON.maintenance_drop_off.name: DEVICE_STATUS.available.name,
    PROVIDER_EVENT_TYPE_REASON.agency_drop_off.name: DEVICE_STATUS.available.name,
    # reserved #
    PROVIDER_EVENT_TYPE_REASON.user_pick_up.name: DEVICE_STATUS.reserved.name,
    # unavailable #
    PROVIDER_EVENT_TYPE_REASON.maintenance.name: DEVICE_STATUS.unavailable.name,
    PROVIDER_EVENT_TYPE_REASON.low_battery.name: DEVICE_STATUS.unavailable.name,
    # removed #
    PROVIDER_EVENT_TYPE_REASON.service_end.name: DEVICE_STATUS.removed.name,
    PROVIDER_EVENT_TYPE_REASON.rebalance_pick_up.name: DEVICE_STATUS.removed.name,
    PROVIDER_EVENT_TYPE_REASON.maintenance_pick_up.name: DEVICE_STATUS.removed.name,
    PROVIDER_EVENT_TYPE_REASON.agency_pick_up.name: DEVICE_STATUS.removed.name,
    # others #
    PROVIDER_EVENT_TYPE_REASON.telemetry.name: DEVICE_STATUS.unknown.name,
    PROVIDER_EVENT_TYPE_REASON.battery_charged.name: DEVICE_STATUS.available.name,
}


OLD_TO_NEW_AGENCY_EVENT = {
    (EVENT_TYPE.service_start.name,): (EVENT_TYPE.service_start.name,),
    (EVENT_TYPE.trip_end.name,): (EVENT_TYPE.trip_end.name,),
    (PROVIDER_EVENT_TYPE_REASON.rebalance_drop_off.name,): (
        EVENT_TYPE.provider_drop_off.name,
    ),
    (PROVIDER_EVENT_TYPE_REASON.maintenance_drop_off.name,): (
        EVENT_TYPE.provider_drop_off.name,
        EVENT_TYPE_REASON.maintenance.name,
    ),
    (EVENT_TYPE.trip_start.name,): (EVENT_TYPE.trip_start.name,),
    (PROVIDER_EVENT_TYPE_REASON.maintenance.name,): (
        EVENT_TYPE.service_end.name,
        EVENT_TYPE_REASON.maintenance.name,
    ),
    (PROVIDER_EVENT_TYPE_REASON.low_battery.name,): (
        EVENT_TYPE.service_end.name,
        EVENT_TYPE_REASON.low_battery.name,
    ),
    (EVENT_TYPE.service_end.name,): (EVENT_TYPE.service_end.name,),
    (PROVIDER_EVENT_TYPE_REASON.rebalance_pick_up.name,): (
        EVENT_TYPE.provider_pick_up.name,
        EVENT_TYPE_REASON.rebalance.name,
    ),
    (PROVIDER_EVENT_TYPE_REASON.maintenance_pick_up.name,): (
        EVENT_TYPE.provider_pick_up.name,
        EVENT_TYPE_REASON.maintenance.name,
    ),
}


def get_new_event_from_old(old_event):
    """
    Maps an old agency event to the new agency event.
    """
    if isinstance(old_event, str):
        old_event = (old_event,)
    return OLD_TO_NEW_AGENCY_EVENT.get(old_event, old_event)


def get_old_event_from_new(event):
    """
    Maps an new agency event to the old one.
    """
    old_event = (
        [
            old_evt
            for old_evt, new_evt in OLD_TO_NEW_AGENCY_EVENT.items()
            if new_evt == event
        ]
        + [event]  # if the event is not in the mapping
    )[0]

    return old_event


def get_provider_reason_from_both_mappings(obj):
    """
    Takes an EventRecord as input (stored with the Agency nomenclature),
    and returns the provider event_type_reason.
    Supports both the old and the new mapping.
    """
    assert hasattr(obj, "event_type")
    use_old_mapping = True

    event = (obj.event_type,)
    if hasattr(obj, "event_type_reason"):
        if isinstance(obj.event_type_reason, str):
            event = (obj.event_type, obj.event_type_reason)
            use_old_mapping = False
        else:
            if (obj.event_type,) in AGENCY_EVENT_TO_PROVIDER_REASON.keys():
                use_old_mapping = False

    if use_old_mapping:
        return OLD_AGENCY_EVENT_TO_PROVIDER_REASON[obj.event_type]
    else:
        return AGENCY_EVENT_TO_PROVIDER_REASON[event]
