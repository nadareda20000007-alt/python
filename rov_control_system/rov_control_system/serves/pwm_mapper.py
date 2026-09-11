from dataclasses import dataclass

@dataclass
class PWMRange:
    min_us: int = 1100
    neutral_us: int = 1500
    max_us: int = 1900

class PWMMapper:
    """Maps normalized joystick axis [-1.0, 1.0] to PWM pulse width in microseconds."""

    def __init__(self, pwm_range: PWMRange = PWMRange()):
        self.range = pwm_range

    def map_value(self, axis_value: float) -> int:
        axis_value = max(-1.0, min(1.0, axis_value))
        if axis_value >= 0:
            pwm = self.range.neutral_us + axis_value * (self.range.max_us - self.range.neutral_us)
        else:
            pwm = self.range.neutral_us + axis_value * (self.range.neutral_us - self.range.min_us)
        return int(round(pwm))

    def map_axes(self, axes: dict) -> dict:
        return {name: self.map_value(v) for name, v in axes.items()}