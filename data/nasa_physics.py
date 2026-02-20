import numpy as np  # type: ignore

class NASAStandardAtmosphere:
    """
    US Standard Atmosphere 1976 Model.
    Provides Atmospheric Density, Temperature, and Pressure based on altitude.
    Reference: NASA-TM-X-74335
    """
    def __init__(self):
        # Layer properties: [Base Altitude (m), Lapse Rate (K/m), Temperature (K), Pressure (Pa), Layer Name]
        self.layers = [
            (0, -0.0065, 288.15, 101325.0, "Troposphere"),
            (11000, 0, 216.65, 22632.1, "Tropopause"),
            (20000, 0.001, 216.65, 5474.89, "Stratosphere 1"),
            (32000, 0.0028, 228.65, 868.02, "Stratosphere 2"),
            (47000, 0, 270.65, 110.91, "Stratopause"),
            (51000, -0.0028, 270.65, 66.94, "Mesosphere 1"),
            (71000, -0.002, 214.65, 3.96, "Mesosphere 2")
        ]
        self.R = 287.058  # Gas constant for air
        self.g0 = 9.80665 # Sea level gravity

    def get_atmospheric_state(self, altitude_m):
        """
        Calculates properties for a given geopotential altitude.
        """
        if altitude_m < 0: altitude_m = 0
        
        # Extended Model for Orbit (> 86km) uses an exponential decay base from the last layer
        if altitude_m > 86000:
            rho_86 = 0.00000696 # kg/m3 approx at 86km
            # Simple orbital decay approximation above Standard Atmosphere limits
            return {"density": rho_86 * np.exp(-(altitude_m - 86000) / 7500.0), "temp_k": 186.87, "pressure_pa": 0.0, "layer": "Thermosphere"}

        # Find the correct layer
        base_h, L, T_base, P_base, layer_name = self.layers[0]
        for i in range(len(self.layers)):
            if altitude_m >= self.layers[i][0]:
                base_h, L, T_base, P_base, layer_name = self.layers[i]
            else:
                break

        h_diff = altitude_m - base_h  # pyre-ignore[58]
        
        # Calculate Temperature
        T = T_base + L * h_diff
        
        # Calculate Pressure
        if L == 0:
            P = P_base * np.exp(-self.g0 * h_diff / (self.R * T_base))
        else:
            P = P_base * (T / T_base) ** (-self.g0 / (L * self.R))
            
        # Calculate Density (Ideal Gas Law: rho = P / (R * T))
        rho = P / (self.R * T)
        
        return {
            "altitude": altitude_m,
            "temp_k": T,
            "pressure_pa": P,
            "density": rho,
            "layer": layer_name
        }

if __name__ == "__main__":
    nasa = NASAStandardAtmosphere()
    # Test at 10km (Jet altitude)
    print(f"NASA 1976 State at 10km: {nasa.get_atmospheric_state(10000)}")
    # Test at 50km (Stratopause)
    print(f"NASA 1976 State at 50km: {nasa.get_atmospheric_state(50000)}")
