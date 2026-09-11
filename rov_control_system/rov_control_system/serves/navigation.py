from rov_control_system.interface.navigation_interface import NavigationService
from rov_control_system.serves.smoothing import Smoother


def apply_deadzone(value: float, threshold: float = 0.05) -> float:
    """Clamps small noise/drift around 0.0 to true zero."""
    if abs(value) < threshold:
        return 0.0
    return value


class NavigationServiceImpl(NavigationService):
    """All the actual logic: map -> smooth -> apply."""

    def __init__(self, thruster_ids: list, smoothing_strategy: str = "linear", **kwargs):
        self.thruster_ids = thruster_ids
        self.strategy = Smoother(smoothing_strategy, **kwargs)
        self._strategy_name = smoothing_strategy

        # Initialize current and target PWM values to neutral (1500 us)
        self._current = {tid: 1500.0 for tid in self.thruster_ids}
        self._target = {tid: 1500.0 for tid in self.thruster_ids}

    def set_smoothing_strategy(self, name: str, **kwargs) -> None:
        """Update the active smoothing strategy."""
        self._strategy_name = name
        self.strategy.switch_strategy(name, **kwargs)

    @property
    def current_strategy(self) -> str:
        """Returns the name of the currently active smoothing strategy."""
        return self._strategy_name

    def update_target(self, axes: list) -> None:
        """
        Maps raw joystick axes [-1.0, 1.0] to target thruster PWMs [1000, 2000].
        Combines X (steering) and Y (forward/backward) with deadzone filtering.
        """
        if not axes:
            return

        # Read axes and apply deadzone filter
        raw_x = axes[0] if len(axes) > 0 else 0.0
        raw_y = axes[1] if len(axes) > 1 else 0.0

        x_axis = apply_deadzone(raw_x)
        y_axis = apply_deadzone(raw_y)

        # Differential mixing layout for left vs right thrusters
        mixing_map = {
            "T1": y_axis + x_axis,  # Left side
            "T2": y_axis - x_axis,  # Right side
            "T3": y_axis + x_axis,  # Left side
            "T4": y_axis - x_axis,  # Right side
        }

        for tid in self.thruster_ids:
            raw_effort = mixing_map.get(tid, y_axis)

            # Clamp combined input range to [-1.0, 1.0]
            clamped_effort = max(-1.0, min(1.0, raw_effort))

            # Scale -1.0..1.0 to 1000..2000 PWM (Neutral = 1500)
            target_pwm = 1500 + int(clamped_effort * 500)
            self._target[tid] = float(max(1000, min(2000, target_pwm)))

    def smooth_step(self) -> dict[str, float]:
        """
        Advances current PWM values toward target values using the active Smoother.
        Call this on every timer loop execution in your ROS node.
        """
        for tid in self.thruster_ids:
            self._current[tid] = self.strategy.step(
                current=self._current[tid],
                target=self._target[tid]
            )
        return self._current