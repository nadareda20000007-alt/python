import os
import sys
from zope.interface import implementer
from rov_control_system.interface.Intr_joystick import IJoystick

IS_WINDOWS = os.name == 'nt'

if IS_WINDOWS:
    import msvcrt
else:
    import select
    import termios
    import tty

@implementer(IJoystick)
class Joystick:
    """
    Joystick class that implements the IJoystick interface.
    """
    def __init__(self):
        self._state = {'x': 0, 'y': 0}
        self._buttons = {}

        if not IS_WINDOWS:
            self._fd = sys.stdin.fileno()
            self._old_term_settings = termios.tcgetattr(self._fd)
            tty.setcbreak(self._fd)

    def __del__(self):
        self.cleanup()

    def cleanup(self):
        """Restore terminal settings on Linux/Mac."""
        if not IS_WINDOWS and hasattr(self, '_old_term_settings'):
            try:
                termios.tcsetattr(self._fd, termios.TCSADRAIN, self._old_term_settings)
            except Exception:
                pass

    def _poll_keyboard(self):
        if IS_WINDOWS:
            if msvcrt.kbhit():
                ch = msvcrt.getch()
                if ch in (b'\xe0', b'\x00'):
                    ch2 = msvcrt.getch()
                    if ch2 == b'M':    # Right arrow
                        self._state['x'] = min(1, self._state['x'] + 1)
                    elif ch2 == b'K':  # Left arrow
                        self._state['x'] = max(-1, self._state['x'] - 1)
                    elif ch2 == b'H':  # Up arrow
                        self._state['y'] = min(1, self._state['y'] + 1)
                    elif ch2 == b'P':  # Down arrow
                        self._state['y'] = max(-1, self._state['y'] - 1)
        else:
            dr, _, _ = select.select([sys.stdin], [], [], 0)
            if dr:
                ch = sys.stdin.read(1)
                if ch == '\x1b':
                    ch2 = sys.stdin.read(1)
                    ch3 = sys.stdin.read(1)
                    if ch2 == '[':
                        if ch3 == 'C':    # Right arrow
                            self._state['x'] = min(1, self._state['x'] + 1)
                        elif ch3 == 'D':  # Left arrow
                            self._state['x'] = max(-1, self._state['x'] - 1)
                        elif ch3 == 'A':  # Up arrow
                            self._state['y'] = min(1, self._state['y'] + 1)
                        elif ch3 == 'B':  # Down arrow
                            self._state['y'] = max(-1, self._state['y'] - 1)

    def get_place(self, axis):
        self._poll_keyboard()
        if axis in (0, 'x'):
            return self._state.get('x', 0)
        elif axis in (1, 'y'):
            return self._state.get('y', 0)
        return 0

    def get_button(self, button):
        self._poll_keyboard()
        return self._buttons.get(button, False)