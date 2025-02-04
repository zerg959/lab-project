from lab_main.lab_app.models.storages import Storage
from lab_main.lab_app.models.users import User
from . objs_for_test import user_for_tests, db_for_tests, storage_for_tests, zone_for_tests

session = db_for_tests()
zone1 = zone_for_tests()
zone2 = zone_for_tests()
storage1 = storage_for_tests(zones=[zone1, zone2])


def test_zone_is_created_and_recorded_in_DB():
    """
    Test if Zone object created and recorded in DB.
    """
    zone = zone_for_tests()
    session.add(zone)
    session.commit()
    assert zone is not None
    assert zone.description is not None
    assert zone.id is not None


def test_zones_added_in_storage():
    """
    Test if more than one Zone object added in Storage.zones.
    """
    session.add_all([zone1, zone2, storage1])
    session.commit()
    assert len(storage1.zones) == 2
    assert zone1 in storage1.zones
    assert zone2 in storage1.zones


def test_zone_can_be_removed():
    """
    Test if Zone object can be removed from in Storage.zones.
    """

    session.add_all([zone1, zone2, storage1])
    storage1.zones.pop(1)
    session.commit()
    assert len(storage1.zones) == 1
    assert not ((zone1 and zone2) in storage1.zones)
    storage1.zones.pop()
    session.commit()
    assert zone1 not in storage1.zones
    assert zone2 not in storage1.zones
    assert len(storage1.zones) == 0
    assert storage1.zones == []
