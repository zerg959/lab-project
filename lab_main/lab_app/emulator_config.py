# lab_app/emulator_config.py
import os
import logging
from emulators.api_emulator import ESPApiEmulator
from flask import Flask


def setup_emulator(app: Flask, port: int = 8001):
    """
    Set up emulator if needs.
    """
    USE_EMULATOR = os.getenv("USE_EMULATOR", "True").lower() == "true"
    # EMULATOR_PORT = int(os.getenv("EMULATOR_PORT", "8000"))
    # EMULATOR_URL = f"http://localhost:{EMULATOR_PORT}/sensor_data"
    EMULATOR_URL = f"http://localhost:{port}/sensor_data"

    if USE_EMULATOR:
        # emulator = ESPApiEmulator(data_source="random", port=EMULATOR_PORT)
        emulator = ESPApiEmulator(data_source="random", port=port)
        emulator.start()
        run_emulator(port=port, emulator=emulator)
        app.logger.info(f"Using API Emulator on {EMULATOR_URL}")
    else:
        app.logger.info("Using Real API")

    # Return emulator api-route for main app.
    return EMULATOR_URL if USE_EMULATOR else os.getenv("REAL_API_URL")
