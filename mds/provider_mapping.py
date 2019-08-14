from mds.enums import EVENT_TYPE, EVENT_TYPE_REASON

# Mappings between Provider and Agency
#
# When we poll providers (with provider API) we cast the event reason
# with PROVIDER_REASON_TO_AGENCY_EVENT because enums don't match
# and we use Agency API nomenclature
# Then when we are ourselves polled we use AGENCY_EVENT_TO_PROVIDER_REASON
# and PROVIDER_REASON_TO_PROVIDER_EVENT_TYPE to be compliant
# with Provider API nomenclature

# Converts a Provider event_type_reason to an Agency event_type
# and event_type_reason (when needed)
PROVIDER_REASON_TO_AGENCY_EVENT = {
    "agency_drop_off": (EVENT_TYPE.agency_drop_off.name,),
    "agency_pick_up": (EVENT_TYPE.agency_pick_up.name,),
    "city_pick_up": (EVENT_TYPE.city_pick_up.name,),
    "low_battery": (EVENT_TYPE.service_end.name, EVENT_TYPE_REASON.low_battery.name),
    "maintenance": (EVENT_TYPE.service_end.name, EVENT_TYPE_REASON.maintenance.name),
    # There is no equivalent on the agency side of maintenance_drop_off. This is the closest
    "maintenance_drop_off": (
        EVENT_TYPE.provider_drop_off.name,
        EVENT_TYPE_REASON.maintenance.name,
    ),
    "maintenance_pick_up": (
        EVENT_TYPE.provider_pick_up.name,
        EVENT_TYPE_REASON.maintenance.name,
    ),
    "rebalance_drop_off": (EVENT_TYPE.provider_drop_off.name,),
    # There is no equivalent on the agency side of rebalance_pick_up.
    "rebalance_pick_up": (
        EVENT_TYPE.provider_pick_up.name,
        EVENT_TYPE_REASON.rebalance.name,
    ),
    "service_end": (EVENT_TYPE.service_end.name,),
    "service_start": (EVENT_TYPE.service_start.name,),
    "user_drop_off": (EVENT_TYPE.trip_end.name,),
    "user_pick_up": (EVENT_TYPE.trip_start.name,),
}

# Converts an Agency event to a Provider event_type_reason
# Try to stay consistent with
# https://github.com/CityOfLosAngeles/mds-core/blob/master/packages/mds-provider/utils.ts
AGENCY_EVENT_TO_PROVIDER_REASON = {
    (EVENT_TYPE.agency_drop_off.name,): "agency_drop_off",
    (EVENT_TYPE.agency_pick_up.name,): "agency_pick_up",
    (EVENT_TYPE.city_pick_up.name,): "city_pick_up",
    # (EVENT_TYPE.battery_charged.name,): "maintenance_drop_off", # Not used anymore
    (EVENT_TYPE.cancel_reservation.name,): "user_drop_off",
    (EVENT_TYPE.deregister.name,): "service_end",
    (EVENT_TYPE.service_end.name, EVENT_TYPE_REASON.low_battery.name): "low_battery",
    (EVENT_TYPE.service_end.name, EVENT_TYPE_REASON.maintenance.name): "maintenance",
    (
        EVENT_TYPE.provider_drop_off.name,
        EVENT_TYPE_REASON.maintenance.name,
    ): "maintenance_drop_off",
    (
        EVENT_TYPE.provider_pick_up.name,
        EVENT_TYPE_REASON.maintenance.name,
    ): "maintenance_pick_up",
    (EVENT_TYPE.provider_drop_off.name,): "rebalance_drop_off",
    (
        EVENT_TYPE.provider_pick_up.name,
        EVENT_TYPE_REASON.rebalance.name,
    ): "rebalance_pick_up",
    (EVENT_TYPE.register.name,): "service_end",
    (EVENT_TYPE.reserve.name,): "user_pick_up",
    (EVENT_TYPE.service_end.name,): "service_end",
    (EVENT_TYPE.service_start.name,): "service_start",
    (EVENT_TYPE.trip_end.name,): "user_drop_off",
    (EVENT_TYPE.trip_enter.name,): "user_pick_up",
    (EVENT_TYPE.trip_leave.name,): "service_end",
    (EVENT_TYPE.trip_start.name,): "user_pick_up",
}

# Inside the Provider API, maps the event_type_reason to the corresponding event_type
PROVIDER_REASON_TO_PROVIDER_EVENT_TYPE = {
    "agency_drop_off": "available",
    "agency_pick_up": "removed",
    "city_pick_up": "removed",
    "low_battery": "unavailable",
    "maintenance": "unavailable",
    "maintenance_drop_off": "available",
    "maintenance_pick_up": "removed",
    "rebalance_drop_off": "available",
    "rebalance_pick_up": "removed",
    "service_start": "available",
    "service_end": "removed",
    "user_drop_off": "available",
    "user_pick_up": "reserved",
}
