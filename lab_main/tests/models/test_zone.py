from lab_main.lab_app.models.storages import Storage
from lab_main.lab_app.models.users import User
from lab_main.lab_app.models.zones import Zone


def test_zone_is_created_and_recorded_in_DB(session, zone_for_tests):
    """
    Test if Zone object created and recorded in DB.
    """
    zone = zone_for_tests()
    session.add(zone)
    session.commit()
    assert zone is not None
    assert zone.description is not None
    assert zone.id is not None


def test_zones_added_in_storage(session, storage_for_tests, zone_for_tests):
    """
    Test if more than one Zone object added in Storage.zones.
    """
    zone1 = zone_for_tests()
    zone2 = zone_for_tests()
    storage1 = storage_for_tests(zones=[zone1, zone2])
    session.add_all([zone1, zone2, storage1])
    session.commit()
    assert len(storage1.zones) == 2
    assert zone1 in storage1.zones
    assert zone2 in storage1.zones
    # add test if one zone can not be linked with 2 storages


def test_zone_can_be_removed(session, storage_for_tests, zone_for_tests):
    """
    Test if Zone object can be removed from in Storage.zones.
    """

    zone1 = zone_for_tests()
    zone2 = zone_for_tests()
    storage1 = storage_for_tests(zones=[zone1, zone2])
    session.add_all([zone1, zone2, storage1])
    session.commit()
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
