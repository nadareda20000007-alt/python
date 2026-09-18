class Validator:

    def __init__(self, tolerance_cm: int = 20):
        self.tolerance_cm = tolerance_cm

    def compare(self, ultrasonic_value: int, infrared_value: int) -> str:
        difference = abs(ultrasonic_value - infrared_value)
        if difference <= self.tolerance_cm:
            return 'Sensor readings consistent'
        else:
            return 'Sensor readings inconsistent'