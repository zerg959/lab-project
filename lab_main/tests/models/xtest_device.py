from lab_main.lab_app.models.devices import Device, Sensor, Regulator

# Создание временной базы данных для тестов


def test_sensor_created_without_PARAMS(sensor_for_tests):
    sensor = sensor_for_tests(description='My Test Description')
    assert sensor.description == 'My Test Description'
    assert sensor.is_outdoor is False
    assert sensor.is_auto_mode_on is False
    assert sensor.device_type == "sensor"
    assert sensor.current_sensor_param == 33.0
    assert sensor.parameters == []  # Пустой список, так как Parameter не реализован
    assert sensor.zone is None
