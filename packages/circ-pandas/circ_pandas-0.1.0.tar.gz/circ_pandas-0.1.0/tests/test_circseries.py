import numpy as np
import pandas as pd
from numpy import testing as npt

from circpandas import circseries


def test_mean() -> None:
    ss = [
        pd.Series([160.0, -170.0]),
        pd.Series([45.0, -45.0, 0.0]),
    ]

    desired = [175.0, 0.0]
    actual = [s.circ.mean(radian=False) for s in ss]
    npt.assert_allclose(actual, desired)


def test_var() -> None:
    ss = [
        pd.Series([90.0, -90.0]),
        pd.Series([90.0, 90.0]),
        pd.Series([45.0, -45.0]),
    ]

    desired = [1.0, 0.0, (1.0 - (1.0 / np.sqrt(2)))]
    actual = [s.circ.var(radian=False) for s in ss]
    npt.assert_allclose(actual, desired)
