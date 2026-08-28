class ThrusterController:
    def __init__(self):
        # 8 Thrusters initialized to 0% thrust
        # Thrusters 1-4: Horizontal | Thrusters 5-8: Vertical
        self.thrusters = [0.0] * 8
        self.is_stopped = False

    def reset_thrusters(self):
        """Stops all 8 thrusters immediately."""
        self.thrusters = [0.0] * 8
        self.is_stopped = False

    def move(self, command: str, power: float = 100.0):
        """
        Maps directional command to thruster output vectors.
        power ranges from 0 to 100%.
        """
        if self.is_stopped:
            return

        p = power / 100.0  # Normalize to range -1.0 to 1.0

        if command == "FORWARD":  # Up Arrow
            self.thrusters[0] = p
            self.thrusters[1] = p
            self.thrusters[2] = p
            self.thrusters[3] = p
            text = "rov is moving FORWARD"
            print(text.rjust(75))
        elif command == "BACKWARD":  # Down Arrow
            self.thrusters[0] = -p
            self.thrusters[1] = -p
            self.thrusters[2] = -p
            self.thrusters[3] = -p
            text = "rov is moving BACKWARD"
            print(text.rjust(60))

        elif command == "TURN_LEFT":  # Left Arrow
            self.thrusters[0] = p     # Starboard Front
            self.thrusters[1] = -p    # Port Front
            self.thrusters[2] = p     # Starboard Rear
            self.thrusters[3] = -p    # Port Rear
            text = "rov is moving TURNING_LEFT"
            print(text.rjust(60))

        elif command == "TURN_RIGHT":  # Right Arrow
            self.thrusters[0] = -p
            self.thrusters[1] = p
            self.thrusters[2] = -p
            self.thrusters[3] = p
            text = "rov is moving TURNING_RIGHT"
            print(text.rjust(60))

        elif command == "STOP":
            self.reset_thrusters()
            self.is_stopped = False

    def display_status(self):
        """Displays formatted thrust levels only for active motors."""
        active_status = [
            f"T{i+1}: {val*100:+.0f}%" 
            for i, val in enumerate(self.thrusters) 
            if val != 0.0
        ]
        
        if active_status:
            print(f"[THRUSTERS] {' | '.join(active_status)}")
        else:
            print("[THRUSTERS] All thrusters idle.")
            
