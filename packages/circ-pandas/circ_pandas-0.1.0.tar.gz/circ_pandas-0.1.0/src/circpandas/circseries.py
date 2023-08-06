import numpy as np
import pandas as pd


@pd.api.extensions.register_series_accessor("circ")
class CircAccessor:
    def __init__(self, pandas_obj: pd.Series) -> None:
        self._obj = pandas_obj

    def mean(self, radian: bool = True) -> float:
        angles = self._obj
        if not radian:
            angles = angles.map(np.deg2rad)
        mean_cosine = np.mean(np.cos(angles))
        mean_sine = np.mean(np.sin(angles))
        mean_angle: float = np.arctan2(mean_sine, mean_cosine)
        if not radian:
            mean_angle = np.rad2deg(mean_angle)
        return mean_angle

    def var(self, radian: bool = True) -> float:
        angles = self._obj
        if not radian:
            angles = angles.map(np.deg2rad)
        mean_cosine = np.mean(np.cos(angles))
        mean_sine = np.mean(np.sin(angles))
        mean_vector_length = np.sqrt(mean_sine ** 2 + mean_cosine ** 2)
        var_angle: float = 1.0 - mean_vector_length
        return var_angle
