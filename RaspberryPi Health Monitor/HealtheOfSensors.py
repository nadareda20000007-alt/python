import random
from Sensors import Sensor

class TempSensor(Sensor):
    def __init__(self, name: str = "Temp", unit: str = "°C"):
        super().__init__(name, unit)

    def read(self):
        # Normal: 30.0°C - 42.0°C | Out-of-bounds (> 50.0°C): ~0.2% chance
        return round(random.uniform(30.0, 50.1), 2)


class VoltageSensor(Sensor):
    def __init__(self, name: str = "Voltage", unit: str = "V"):
        super().__init__(name, unit)

    def read(self):
        # Normal: 11.8V - 13.5V | Out-of-bounds (< 10.8V or > 14.5V): ~0.5% chance
        return round(random.uniform(10.78, 14.52), 2)


class CpuSensor(Sensor):
    def __init__(self, name: str = "CPU Load", unit: str = "%"):
        super().__init__(name, unit)

    def read(self):
        # Normal: 20.0% - 65.0% | Out-of-bounds (> 85.0%): ~0.3% chance
        return round(random.uniform(20.0, 85.2), 2)