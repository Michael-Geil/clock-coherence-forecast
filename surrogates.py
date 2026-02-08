# surrogates.py
import numpy as np

def phase_randomize_in_mask(XB: np.ndarray, mask: np.ndarray, rng: np.random.Generator) -> np.ndarray:
   """
   Phase-randomize XB only inside a boolean frequency mask (rFFT domain).
   Preserves amplitude spectrum everywhere; randomizes phase only where mask==True.
   """
   ph = np.angle(XB).copy()
   ph[mask] = rng.uniform(0.0, 2.0*np.pi, size=int(mask.sum()))
   return np.abs(XB) * np.exp(1j * ph)

def circular_shift_time_series(x: np.ndarray, rng: np.random.Generator) -> np.ndarray:
   """
   Circularly shift a real time series by a random integer offset.
   """
   n = len(x)
   k = int(rng.integers(0, n))
   return np.roll(x, k)

def surrogate_p_value(null_values: np.ndarray, real_value: float) -> float:
   """
   Conservative Monte Carlo p-value with +1 correction.
   """
   null_values = np.asarray(null_values)
   return float((np.sum(null_values >= real_value) + 1) / (len(null_values) + 1))


