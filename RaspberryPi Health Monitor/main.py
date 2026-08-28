import time
from Controller import ThrusterController
from Keyboard import KeyboardInput
from HealtheOfSensors import TempSensor, CpuSensor, VoltageSensor


def flush_input_buffer():
    """Flushes lingering keystrokes so old key events are discarded."""
    while KeyboardInput.get_key_non_blocking() is not None:
        pass


def main():
    temp_sensor = TempSensor()
    volt_sensor = VoltageSensor()
    cpu_sensor = CpuSensor()
    rov = ThrusterController()

    lockout_until = 0.0  # Timestamp for non-blocking health lockout

    print("\n--- ROV Keyboard Motion Control ---")
    print("Use Arrow Keys to drive. Press 'q' to quit.")

    try:
        while True:
            current_time = time.time()

            # Display Telemetry Header
            text = "--Health Reading--"
            print(text.rjust(100))
            temp_sensor.report()
            volt_sensor.report()
            cpu_sensor.report()

            # Get numeric values for logic checks
            # Note: Replace .read() with .value or whatever getter method your class defines
            t_val = temp_sensor.read() if hasattr(temp_sensor, 'read') else temp_sensor.value
            v_val = volt_sensor.read() if hasattr(volt_sensor, 'read') else volt_sensor.value
            c_val = cpu_sensor.read() if hasattr(cpu_sensor, 'read') else cpu_sensor.value

            # --- Independent Health Safety Check ---
            if t_val > 50.0 or t_val < 0.0 or c_val > 85.0 or v_val < 10.8 or v_val > 14.5:
                print("Warning: error in the health occurs!")
                rov.reset_thrusters()
                time.sleep(5)
                rov.is_stopped = False


            # --- Motion Processing ---
            if current_time < lockout_until:
                # Still inside safety lockout period: flush keys and force STOP
                flush_input_buffer()
                rov.move("STOP")
            else:
                rov.is_stopped = False
                
                # Fetch only the MOST RECENT key press available right now
                key = KeyboardInput.get_key_non_blocking()

                if key == '\x1b[A':        # Up Arrow
                    rov.move("FORWARD")
                elif key == '\x1b[B':      # Down Arrow
                    rov.move("BACKWARD")
                elif key == '\x1b[D':      # Left Arrow
                    rov.move("TURN_LEFT")
                elif key == '\x1b[C':      # Right Arrow
                    rov.move("TURN_RIGHT")
                elif key == 'q':
                    rov.reset_thrusters()
                    print("\nExiting controller.")
                    break
                else:
                    rov.move("STOP")

            # Display thruster status
            rov.display_status()
            
            # Flush any remaining key queue build-up before the next cycle
            flush_input_buffer()
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("\nShutdown.")


if __name__ == "__main__":
    main()