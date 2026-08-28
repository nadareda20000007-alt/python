import os
import sys

# Platform detection
IS_WINDOWS = os.name == 'nt'

if IS_WINDOWS:
    import msvcrt
else:
    import select
    import termios
    import tty

class KeyboardInput:
    @staticmethod
    def get_key_non_blocking():
        """Reads a single keypress without blocking the execution loop."""
        if IS_WINDOWS:
            if msvcrt.kbhit():
                key = msvcrt.getch()
                # Handle extended arrow key prefix in Windows (0x00 or 0xE0)
                if key in (b'\x00', b'\xe0'):
                    arrow = msvcrt.getch()
                    arrow_map = {
                        b'H': '\x1b[A',  # Up Arrow
                        b'P': '\x1b[B',  # Down Arrow
                        b'K': '\x1b[D',  # Left Arrow
                        b'M': '\x1b[C',  # Right Arrow
                    }
                    return arrow_map.get(arrow, None)
                try:
                    return key.decode('utf-8')
                except UnicodeDecodeError:
                    return None
            return None
        else:
            # Linux / Raspberry Pi OS non-blocking read
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(sys.stdin.fileno())
                dr, _, _ = select.select([sys.stdin], [], [], 0.01)
                if dr:
                    key = sys.stdin.read(1)
                    if key == '\x1b':
                        dr2, _, _ = select.select([sys.stdin], [], [], 0.01)
                        if dr2:
                            key += sys.stdin.read(2)
                    return key
                return None
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)