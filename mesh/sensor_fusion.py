import numpy as np  # type: ignore

class MultiSensorFusion:
    """
    Merges Vision (CNN), Radar, and IR signatures into a unified Tracking Tensor.
    """
    def __init__(self):
        self.fusion_weights = {
            "visual": 0.4,
            "radar": 0.4,
            "infrared": 0.2
        }

    def fuse_signatures(self, visual_data, radar_data, ir_data):
        """
        Combines disparate sensor inputs.
        Input: Tensors/Vectors from each sensor head.
        """
        # Ensure all data is normalized or handled in the same space
        # Here we demonstrate a simple weighted average fusion
        master_tensor = (
            self.fusion_weights["visual"] * visual_data +
            self.fusion_weights["radar"] * radar_data +
            self.fusion_weights["infrared"] * ir_data
        )
        
        # Reliability check: if one sensor shows high variance, reduce its weight
        confidence = 1.0 - np.std([visual_data, radar_data, ir_data])
        
        return master_tensor, confidence

if __name__ == "__main__":
    fusion = MultiSensorFusion()
    v, r, i = np.array([0.9, 0.1]), np.array([0.85, 0.15]), np.array([0.92, 0.08])
    master, conf = fusion.fuse_signatures(v, r, i)
    print(f"Master Tracking Tensor: {master} | Confidence: {conf:.4f}")
