import random
import json
import time
from threading import Thread
from http.server import HTTPServer, BaseHTTPRequestHandler

'''
test requests:
curl -X POST http://localhost:8001/sensor_data \
-H "Content-Type: application/json" \
-d '{"temperature": 25.5, "humidity": 60, "co2": 450}'
'''


class MockSensorDataHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, emulator=None, **kwargs):  # Add emulator parameter
        self.emulator = emulator  # Store the emulator instance
        super().__init__(*args, **kwargs)

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        try:
            # Try to parse the incoming data as JSON to simulate a POST request
            data = json.loads(post_data.decode('utf-8'))
            print(f"Received {data}")  # log data received by ESP
        except json.JSONDecodeError:
            print("Received data but was not valid JSON.")

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response = bytes('{"status": "success"}', 'utf-8')  # Simple feedback
        self.wfile.write(response)

    def do_GET(self):
        """Обработка GET-запросов для тестирования"""
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response = json.dumps({
            "status": "GET request received",
            "available_methods": ["POST", "GET"],
            "description": "Use POST to send sensor data"
        })
        self.wfile.write(response.encode('utf-8'))


def run_emulator(port=8001, emulator=None):
    """Start a mock ESP server to simulate sensor data being posted."""
    server_address = ('', port)
    httpd = HTTPServer(
        server_address,
        lambda *args, **kwargs: MockSensorDataHandler(
            *args,
            emulator=emulator,
            **kwargs)
            )
    print(f"Starting mock ESP server on port {port}...")
    httpd.serve_forever()


class ESPApiEmulator:
    """
    Emulates the API of an ESP8266 device.
    """

    def __init__(self, data_source="random", data_file=None, port=8001):
        """
        Initializes the emulator.

        Args:
            data_source: "random" (generate random data) or "file" (read data from file).
            data_file: Path to the data file (if data_source is "file").
        """
        self.data_source = data_source
        self.data_file = data_file
        self.port = port
        self.server_thread = None

    def get_sensor_data(self):
        """
        Returns simulated sensor data.
        """
        if self.data_source == "random":
            temperature = round(random.uniform(15, 30), 1)
            humidity = round(random.uniform(40, 80), 1)
            co2 = random.randint(400, 1000)
            return {
                "temperature": temperature,
                "humidity": humidity,
                "co2": co2
                }
        elif self.data_source == "file":
            if not self.data_file:
                raise ValueError(
                    "Data file must be specified when data_source is 'file'"
                    )
            try:
                with open(self.data_file, "r") as f:
                    data = json.load(f)
                    return data
            except FileNotFoundError:
                raise FileNotFoundError(
                    f"Data file not found: {self.data_file}"
                    )
        else:
            raise ValueError(f"Invalid data source: {self.data_source}")

    def get_regulator_data(self):
        """
        Returns simulated sensor data.
        """
        if self.data_source == "random":
            temperature = round(random.uniform(15, 30), 1)
            humidity = round(random.uniform(40, 80), 1)
            co2 = random.randint(400, 1000)
            return {
                "temperature": temperature,
                "humidity": humidity,
                "co2": co2
                }
        elif self.data_source == "file":
            if not self.data_file:
                raise ValueError(
                    "Data file must be specified when data_source is 'file'"
                    )
            try:
                with open(self.data_file, "r") as f:
                    data = json.load(f)
                    return data
            except FileNotFoundError:
                raise FileNotFoundError(
                    f"Data file not found: {self.data_file}"
                    )
        else:
            raise ValueError(f"Invalid data source: {self.data_source}")

    def start(self):
        """
        Starts the emulator.
        """
        # Basic setup, could be expanded to actually run 
        # a mini-server to handle requests
        print(f"ESP8266 API Emulator started (source: {self.data_source})")

    def run_emulator_in_thread(self):
        self.server_thread = Thread(target=run_emulator, args=(self.port,))
        self.server_thread.daemon = True  # Daemon threads exit when the main program exits
        self.server_thread.start()
        print(f"Emulator running in thread on port {self.port}.")


# Пример использования
if __name__ == "__main__":
    emulator = ESPApiEmulator(data_source="random", port=8001)
    emulator.start()
    emulator.run_emulator_in_thread()

    try:
        while True:
            sensor_data = emulator.get_sensor_data()
            print(f"Simulated sensor {sensor_data}")
            time.sleep(5)  # Adjust sleep time as needed
    except KeyboardInterrupt:
        print("Emulator stopped.")
