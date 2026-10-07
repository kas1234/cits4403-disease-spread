"""Tests for the statistics helpers in utils/stats.py."""

import math

import pandas as pd
import pytest

from utils.stats import is_major_outbreak, mean_ci, summarise


def test_mean_ci_of_known_values():
    mean, ci = mean_ci([1, 2, 3, 4])
    # sample std = sqrt(5/3), so the half-width is 1.96 * std / 2
    assert mean == pytest.approx(2.5)
    assert ci == pytest.approx(1.96 * math.sqrt(5 / 3) / 2)


def test_mean_ci_of_identical_values_has_zero_width():
    mean, ci = mean_ci([0.4, 0.4, 0.4])
    assert mean == pytest.approx(0.4)
    assert ci == pytest.approx(0.0)


def test_mean_ci_single_value_and_empty_input():
    assert mean_ci([0.7]) == (0.7, 0.0)
    with pytest.raises(ValueError):
        mean_ci([])


def test_summarise_groups_correctly():
    df = pd.DataFrame({"topology": ["a", "a", "b", "b"], "final_size": [0.2, 0.4, 0.6, 0.6]})
    result = summarise(df, ["topology"], "final_size").set_index("topology")
    assert result.loc["a", "mean"] == pytest.approx(0.3)
    assert result.loc["b", "mean"] == pytest.approx(0.6)
    assert result.loc["b", "ci95"] == pytest.approx(0.0)


def test_is_major_outbreak_threshold():
    assert is_major_outbreak(0.5)
    assert not is_major_outbreak(0.1)  # exactly at the threshold does not count
    assert not is_major_outbreak(0.01)
