# from lab_main.lab_app.models.devices import Device, Sensor, Regulator

def test_sensor_created_without_PARAMS(sensor_for_tests):
    """
    Test if sensor created.
    """
    sensor = sensor_for_tests(description='Sensor Test Description')
    assert sensor.description == 'Sensor Test Description'
    assert sensor.is_outdoor is False
    assert sensor.is_auto_mode_on is False
    assert sensor.device_type == "sensor"
    assert sensor.current_sensor_param == 33.0
    assert sensor.zone is None


def test_regulator_creates_without_PARAMS(regulator_for_tests):
    """
    Test if regulator created.
    """
    regulator = regulator_for_tests(
        description="Regulator Test Description")
    assert regulator.description == "Regulator Test Description"
    assert regulator.is_outdoor is False
    assert regulator.is_auto_mode_on is False
    assert regulator.device_type == "regulator"
    assert regulator.zone is None
