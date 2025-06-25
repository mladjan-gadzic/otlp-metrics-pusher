import os
import time
import random
from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.metrics._internal.observation import Observation

OTLP_ENDPOINT = os.getenv("OTLP_ENDPOINT", "http://localhost:4000/v1/otlp/v1/metrics")
EXPORT_INTERVAL_MS = 5000
ROOMS = 10_000
DEVICES_PER_ROOM = 10

# Assign a random GAUGE_INDEX between 1 and 10,000
GAUGE_INDEX = random.randint(1, 10_000)
print(f"🎲 Random GAUGE_INDEX selected: {GAUGE_INDEX}")

exporter = OTLPMetricExporter(endpoint=OTLP_ENDPOINT)
reader = PeriodicExportingMetricReader(exporter, export_interval_millis=EXPORT_INTERVAL_MS)

provider = MeterProvider(metric_readers=[reader])
metrics.set_meter_provider(provider)
meter = metrics.get_meter("greptime.loadgen")

def callback(options):
    observations = []
    start_room = GAUGE_INDEX * ROOMS
    for room in range(start_room, start_room + ROOMS):
        for device in range(DEVICES_PER_ROOM):
            val = random.uniform(10.0, 45.0)
            labels = {
                "room": f"room_{room}",
                "device": f"device_{device}",
                "chunk": f"block_{GAUGE_INDEX}"
            }
            observations.append(Observation(val, attributes=labels))
    print(f"[G{GAUGE_INDEX}] ✅ Pushed {len(observations)} metrics")
    return observations

meter.create_observable_gauge(
    name=f"synthetic_temperature_block_{GAUGE_INDEX}",
    description="High-scale temperature test",
    unit="celsius",
    callbacks=[callback],
)

print(f"[G{GAUGE_INDEX}] 🚀 Running: pushing 100k metrics every {EXPORT_INTERVAL_MS//1000}s to {OTLP_ENDPOINT}")
while True:
    time.sleep(EXPORT_INTERVAL_MS / 1000)