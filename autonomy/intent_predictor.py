import tensorflow as tf  # type: ignore
from tensorflow.keras import layers  # type: ignore
import numpy as np  # type: ignore

class IntentPredictor:
    """
    Sequential Model (LSTM) to predict next 5 seconds of target intent.
    Learns from typical aircraft flight envelopes.
    """
    def __init__(self, seq_len=20, feature_dim=6):
        self.seq_len = seq_len
        self.feature_dim = feature_dim
        self.model = self._build_model()

    def _build_model(self):
        model = tf.keras.Sequential([
            layers.Input(shape=(self.seq_len, self.feature_dim)),
            layers.LSTM(128, return_sequences=True),
            layers.LSTM(64),
            layers.Dense(32, activation='relu'),
            layers.Dense(5 * 3, name="prediction_output") # 5 seconds of (x,y,z) deltas
        ])
        model.compile(optimizer='adam', loss='mse')
        return model

    def predict_evasion(self, history):
        """
        Input: history tensor of shape (1, seq_len, 6)
        Output: predicted trajectory of shape (5, 3)
        """
        pred = self.model.predict(history)
        return pred.reshape(5, 3)

# Example Usage
if __name__ == "__main__":
    predictor = IntentPredictor()
    # Mock history: 20 steps of [x,y,z,vx,vy,vz]
    mock_history = np.random.randn(1, 20, 6).astype(np.float32)
    evasion = predictor.predict_evasion(mock_history)
    print(f"Predicted Evasive Maneuver (Next 5s deltas): \n{evasion}")
