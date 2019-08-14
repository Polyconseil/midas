from mds.enums import DEVICE_STATUS, EVENT_TYPE, EVENT_TYPE_REASON

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
    ########## available ##########
    "service_start": (EVENT_TYPE.service_start.name,),
    "user_drop_off": (EVENT_TYPE.trip_end.name,),
    "rebalance_drop_off": (EVENT_TYPE.provider_drop_off.name,),
    # There is no equivalent on the agency side of maintenance_drop_off. This is the closest
    "maintenance_drop_off": (
        EVENT_TYPE.provider_drop_off.name,
        EVENT_TYPE_REASON.maintenance.name,
    ),
    "agency_drop_off": (EVENT_TYPE.agency_drop_off.name,),
    ########## reserved ##########
    "user_pick_up": (EVENT_TYPE.trip_start.name,),
    ########## unavailable ##########
    "maintenance": (EVENT_TYPE.service_end.name, EVENT_TYPE_REASON.maintenance.name),
    "low_battery": (EVENT_TYPE.service_end.name, EVENT_TYPE_REASON.low_battery.name),
    ########## removed ##########
    "service_end": (EVENT_TYPE.service_end.name,),
    # There is no equivalent on the agency side of rebalance_pick_up.
    "rebalance_pick_up": (
        EVENT_TYPE.provider_pick_up.name,
        EVENT_TYPE_REASON.rebalance.name,
    ),
    "maintenance_pick_up": (
        EVENT_TYPE.provider_pick_up.name,
        EVENT_TYPE_REASON.maintenance.name,
    ),
    "agency_pick_up": (EVENT_TYPE.city_pick_up.name,),
}

# Converts an Agency event to a Provider event_type_reason
# Try to stay consistent with
# https://github.com/CityOfLosAngeles/mds-core/blob/master/packages/mds-provider/utils.ts
AGENCY_EVENT_TO_PROVIDER_REASON = {
    (EVENT_TYPE.register.name,): "service_end",
    (EVENT_TYPE.service_start.name,): "service_start",
    (EVENT_TYPE.service_end.name,): "service_end",
    (EVENT_TYPE.service_end.name, EVENT_TYPE_REASON.low_battery.name): "low_battery",
    (EVENT_TYPE.service_end.name, EVENT_TYPE_REASON.maintenance.name): "maintenance",
    (EVENT_TYPE.service_end.name, EVENT_TYPE_REASON.compliance.name): "service_end",
    (EVENT_TYPE.service_end.name, EVENT_TYPE_REASON.off_hours.name): "service_end",
    (EVENT_TYPE.provider_drop_off.name,): "rebalance_drop_off",
    (
        EVENT_TYPE.provider_drop_off.name,
        EVENT_TYPE_REASON.maintenance.name,
    ): "maintenance_drop_off",  # In the provider spec
    (EVENT_TYPE.provider_pick_up.name,): "service_end",
    (
        EVENT_TYPE.provider_pick_up.name,
        EVENT_TYPE_REASON.rebalance.name,
    ): "rebalance_pick_up",
    (
        EVENT_TYPE.provider_pick_up.name,
        EVENT_TYPE_REASON.maintenance.name,
    ): "maintenance_pick_up",
    (
        EVENT_TYPE.provider_pick_up.name,
        EVENT_TYPE_REASON.charge.name,
    ): "maintenance_pick_up",
    (
        EVENT_TYPE.provider_pick_up.name,
        EVENT_TYPE_REASON.compliance.name,
    ): "service_end",
    # no city_pick_up in provider's spec
    (EVENT_TYPE.city_pick_up.name,): "agency_pick_up",
    (EVENT_TYPE.reserve.name,): "user_pick_up",
    (EVENT_TYPE.cancel_reservation.name,): "user_drop_off",
    (EVENT_TYPE.trip_start.name,): "user_pick_up",
    (EVENT_TYPE.trip_enter.name,): "user_pick_up",
    (EVENT_TYPE.trip_leave.name,): "service_end",
    (EVENT_TYPE.trip_end.name,): "user_drop_off",
    (EVENT_TYPE.deregister.name,): "service_end",
    (EVENT_TYPE.deregister.name, EVENT_TYPE_REASON.missing.name): "service_end",
    (EVENT_TYPE.deregister.name, EVENT_TYPE_REASON.decommissioned.name): "service_end",
    # Not in the MDS agency spec: probably not used
    (EVENT_TYPE.agency_drop_off.name,): "agency_drop_off",  # not used
    (EVENT_TYPE.agency_pick_up.name,): "agency_pick_up",  # not used
    (EVENT_TYPE.battery_charged.name,): "maintenance_drop_off",  # not used
}

# Inside the Provider API, maps the event_type_reason to the corresponding event_type
# https://github.com/CityOfLosAngeles/mobility-data-specification/tree/dev/provider
PROVIDER_EVENT_TYPE_REASON_TO_EVENT_TYPE = {
    ########## available ##########
    EVENT_TYPE.service_start.name: DEVICE_STATUS.available.name,
    EVENT_TYPE.user_drop_off.name: DEVICE_STATUS.available.name,
    EVENT_TYPE.rebalance_drop_off.name: DEVICE_STATUS.available.name,
    EVENT_TYPE.maintenance_drop_off.name: DEVICE_STATUS.available.name,
    EVENT_TYPE.agency_drop_off.name: DEVICE_STATUS.available.name,
    ########## reserved ##########
    EVENT_TYPE.user_pick_up.name: DEVICE_STATUS.reserved.name,
    ########## unavailable ##########
    EVENT_TYPE.maintenance.name: DEVICE_STATUS.unavailable.name,
    EVENT_TYPE.low_battery.name: DEVICE_STATUS.unavailable.name,
    ########## removed ##########
    EVENT_TYPE.service_end.name: DEVICE_STATUS.removed.name,
    EVENT_TYPE.rebalance_pick_up.name: DEVICE_STATUS.removed.name,
    EVENT_TYPE.maintenance_pick_up.name: DEVICE_STATUS.removed.name,
    EVENT_TYPE.agency_pick_up.name: DEVICE_STATUS.removed.name,
}
