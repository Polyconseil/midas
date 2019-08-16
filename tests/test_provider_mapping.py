from mds.provider_mapping import (
    AGENCY_EVENT_TO_PROVIDER_REASON,
    OLD_AGENCY_EVENT_TO_PROVIDER_REASON,
    OLD_PROVIDER_REASON_TO_AGENCY_EVENT,
    OLD_TO_NEW_AGENCY_EVENT,
    PROVIDER_REASON_TO_AGENCY_EVENT,
)

# This file tests the different functions of this old and new mapping:
# Old:
# Provider    --old_p_a-->    Agency    --old_a_p-->    Provider
# New:                   --old_to_new_a--
# Provider    --new_p_a-->    Agency    --new_a_p-->    Provider


def test_provider_agency_mapping():
    """
    Checks that the bidirectional mappings are kind of consistent.
    new_a_p ○ new_p_a = id
    """
    for provider_reason, agency_event in PROVIDER_REASON_TO_AGENCY_EVENT.items():
        assert AGENCY_EVENT_TO_PROVIDER_REASON[agency_event] == provider_reason


def test_old_provider_agency_mapping():
    """
    Checks that the old bidirectional mappings are kind of consistent
    old_a_p ○ old_p_a = id
    """
    for provider_reason, agency_event in OLD_PROVIDER_REASON_TO_AGENCY_EVENT.items():
        assert OLD_AGENCY_EVENT_TO_PROVIDER_REASON[agency_event] == provider_reason


def test_old_to_new_is_same_as_new():
    """
    Checks that when we apply the migration to the old events,
    we have the same result as with the new mappings.
    old_to_new_a ○ old_p_a = new_p_a
    """
    for reason, old_agency_event in OLD_PROVIDER_REASON_TO_AGENCY_EVENT.items():
        agency_event = OLD_TO_NEW_AGENCY_EVENT[(old_agency_event,)]
        new_agency_event = PROVIDER_REASON_TO_AGENCY_EVENT[reason]
        assert agency_event == new_agency_event


def test_migration_new_idem():
    """
    Checks that when we apply the old_to_new migration to the new events,
    we don't change anything.
    old_to_new_a(new)= new
    """
    for _, agency_event in PROVIDER_REASON_TO_AGENCY_EVENT.items():
        new_agency_event = OLD_TO_NEW_AGENCY_EVENT.get(agency_event, agency_event)
        assert agency_event == new_agency_event


def test_migration_idempotent():
    """
    Checks that applying the old to new mapping twice is the same as applying it once
    old_to_new_a ○ old_to_new_a = old_to_new_a
    """
    for _, agency_event in OLD_PROVIDER_REASON_TO_AGENCY_EVENT.items():
        new_agency_event = OLD_TO_NEW_AGENCY_EVENT.get(agency_event, agency_event)
        new_new_agency_event = OLD_TO_NEW_AGENCY_EVENT.get(
            new_agency_event, new_agency_event
        )
        assert new_agency_event == new_new_agency_event
