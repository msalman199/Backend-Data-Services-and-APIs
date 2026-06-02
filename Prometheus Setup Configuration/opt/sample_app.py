from prometheus_client import start_http_server, Counter, Gauge
import time
import random

# TODO: Create a Counter metric named 'app_requests_total' with description 'Total app requests'
requests_counter = None

# TODO: Create a Gauge metric named 'app_temperature' with description 'Current temperature'
temperature_gauge = None

def process_request():
    """Simulate processing a request"""
    # TODO: Increment the requests counter
    pass

def update_temperature():
    """Simulate temperature reading"""
    # TODO: Set the temperature gauge to a random value between 20 and 30
    pass

if __name__ == '__main__':
    # Start metrics server on port 8000
    start_http_server(8000)
    print("Metrics server started on port 8000")
    
    while True:
        process_request()
        update_temperature()
        time.sleep(5)
