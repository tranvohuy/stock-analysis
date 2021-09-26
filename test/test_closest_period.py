# to run in command line: python - m pytest -v
import numpy as np

# from pytest import mark.parameterize as parametrize
import pytest
from analysis_utils.calculations import closest_period, shift_vector_difference


@pytest.mark.parametrize(
    "input, output",
    [
        [np.array([1, 2, 3, 4]), [1, 1, 1]],
        [np.array([1, 2, 3, 5]), [1, 1, 2]],
    ],
)
def test_shift_vector_differe_1(input, output):
    """
    Test that it can sum a list of integers
    """
    assert list(shift_vector_difference(input)) == output


@pytest.mark.parametrize(
    "input, output",
    [
        [np.array([1, 2, 4]), [1, 1]],
        [np.array([1, 2, 3, 6]), [1, 1, 2]],
    ],
)
def test_shift_vector_difference_2(input, output):
    """ """
    assert list(shift_vector_difference(input)) != output


def test_closest_period():
    """
    Test that it can sum a list of integers
    """
    base_vector = [1, 2]
    vector = [1, 2, 3, 4]
    (ind, distance) = closest_period(base_vector, vector)
    assert ind == 0
    assert distance == 0
    vector = [3, 4, 1, 2]
    (ind, distance) = closest_period(base_vector, vector)
    assert ind == 2
    assert distance == 0
