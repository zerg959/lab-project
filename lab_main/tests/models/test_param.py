def test_if_param_created(param_for_tests, sensor_for_tests):
    sensor = sensor_for_tests(description='Test sensor')
    parameter = param_for_tests(parameter_name="humidity",
                                parameter_unit="%",
                                description="Test humidity param description",
                                sensors=[sensor]
                                )
    assert parameter.sensors is not None
    assert parameter.description == "Test humidity param description"
    assert parameter.parameter_name == "humidity"
    assert parameter.parameter_unit == "%"
    assert len(parameter.sensors) == 1
