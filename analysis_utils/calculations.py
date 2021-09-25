from typing import List
import numpy as np
from numpy import linalg as LA


def shift_vector_difference(vector: np.array) -> np.array:

    return vector[1:] - vector[:-1]


def closest_behavior(base_vector: List[float], vector: List[float], metric: str = "l2"):
    n = len(base_vector)
    base_vector = np.array(base_vector)
    vector = np.array(vector)
    if n < 2:
        raise ValueError(f"length of base_vector {base_vector} needs to be >1")
    base_vector_shift = base_vector[1:] - base_vector[:-2]
    print(base_vector_shift)
    # print(vector, vector[1:], vector[:-2])
    shift_distance = shift_vector_difference(vector)
    (ind, distance) = closest_period(base_vector_shift, shift_distance)
    print(f"ind = {ind}, distance = {distance}")

    return (ind, distance)


def closest_period(base_vector: List[float], vector: List[float], metric: str = "l2"):
    """

    :param base_vector:
    :param vector:
    :param metric:
    :return:
    """
    n = len(base_vector)
    base_vector = np.array(base_vector)
    # print(base_vector)
    distance_vector = (
        np.array([vector[i : i + n] for i in range(0, len(vector) - n + 1)])
        - base_vector
    )
    distance_list = LA.norm(distance_vector, axis=1)
    return (np.argmin(distance_list), np.min(distance_list))
