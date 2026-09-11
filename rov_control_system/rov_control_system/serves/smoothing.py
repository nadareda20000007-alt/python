from rov_control_system.interface.smoothing_interface import SmoothingFunction

def linear_step(current: float, target: float, step_size: float = 20.0) -> float:
    """Constant slew rate — moves toward target by a fixed step each tick."""
    diff = target - current
    if abs(diff) <= step_size:
        return target
    return current + step_size * (1 if diff > 0 else -1)


def exponential_step(current: float, target: float, alpha: float = 0.2) -> float:
    """Moves a fixed fraction of the remaining gap each tick (EMA). Higher alpha = faster."""
    if not 0 < alpha <= 1:
        raise ValueError("alpha must be in (0, 1]")
    new_value = current + alpha * (target - current)
    return target if abs(target - new_value) <= 0.5 else new_value


SMOOTHING_FUNCTIONS: dict[str, SmoothingFunction] = {
    "linear": linear_step, 
    "exponential": exponential_step,
}


class Smoother:
    def __init__(self, strategy: str = "linear", **kwargs):
        self._func: SmoothingFunction = SMOOTHING_FUNCTIONS[strategy]
        self._kwargs = kwargs

    def step(self, current: float, target: float) -> float:
        return self._func(current, target, **self._kwargs)

    def switch_strategy(self, name: str, **kwargs) -> None:
        self._func = SMOOTHING_FUNCTIONS[name]
        self._kwargs = kwargs