"""
Small statistics helpers for summarising repeated simulation runs.

Every simulation is random, so each parameter combination is run many times
and we report the mean together with a 95% confidence interval.
"""

import numpy as np
import pandas as pd

# A run counts as a "major outbreak" if more than this fraction of the
# population was infected. Smaller runs are outbreaks that died out early.
MAJOR_OUTBREAK = 0.10


def mean_ci(values, z: float = 1.96) -> tuple[float, float]:
    """Return the mean and the half-width of its 95% confidence interval.

    The interval uses the normal approximation: z * s / sqrt(n), where s is
    the sample standard deviation and n the number of repetitions.
    """
    values = np.asarray(values, dtype=float)
    n = len(values)
    if n == 0:
        raise ValueError("Cannot summarise an empty list of values.")
    if n == 1:
        return float(values[0]), 0.0
    return float(values.mean()), float(z * values.std(ddof=1) / np.sqrt(n))


def summarise(df: pd.DataFrame, by: list[str], column: str) -> pd.DataFrame:
    """Mean and 95% CI half-width of `column` for every group in `by`."""
    rows = []
    for key, group in df.groupby(by):
        mean, ci95 = mean_ci(group[column])
        key = key if isinstance(key, tuple) else (key,)
        rows.append({**dict(zip(by, key)), "mean": mean, "ci95": ci95})
    return pd.DataFrame(rows)


def is_major_outbreak(final_size: float, threshold: float = MAJOR_OUTBREAK) -> bool:
    """True if the outbreak infected more than `threshold` of the population."""
    return final_size > threshold
