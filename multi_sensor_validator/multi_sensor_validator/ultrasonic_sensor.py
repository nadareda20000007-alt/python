import random


class Ultrasonic:
    """Plain class that simulates an ultrasonic distance sensor."""

    def __init__(self, min_range_cm: int = 10, max_range_cm: int = 200):
        self.min_range_cm = min_range_cm
        self.max_range_cm = max_range_cm

    def read(self) -> int:
        """Return a simulated distance reading in cm."""
        return random.randint(self.min_range_cm, self.max_range_cm)