import numpy as np  # type: ignore

class IntegrityVerifier:
    """
    Sanity Check module for flagged sensor hacks or algorithm failures.
    Ensures output trajectories are physically possible.
    """
    def __init__(self):
        self.max_velocity = 3000.0 # m/s (Hypersonic limit)
        self.max_accel = 150.0     # m/s^2 (Structural limit)

    def verify_trajectory(self, trajectory_points):
        """
        Input: List of [x, y, z] points over time.
        """
        for i in range(1, len(trajectory_points)):
            p1 = trajectory_points[i-1]
            p2 = trajectory_points[i]
            
            # Calculate derived velocity
            dist = np.linalg.norm(p2 - p1)
            # Assuming dt = 0.1s
            velocity = dist / 0.1
            
            if velocity > self.max_velocity:
                return False, f"CRITICAL: Velocity {velocity:.2f} m/s violates physics (Sensor Hack?)"
            
        return True, "Trajectory Integrity Verified: NOMINAL"

if __name__ == "__main__":
    verifier = IntegrityVerifier()
    points = [np.array([0,0,0]), np.array([500,0,0])] # 500m in 0.1s = 5000 m/s
    ok, msg = verifier.verify_trajectory(points)
    print(f"Sanity Check: {msg}")
