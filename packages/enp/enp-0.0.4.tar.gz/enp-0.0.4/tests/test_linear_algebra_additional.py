import numpy as np
from enp.linear_algebra_additional import *


def test_number_of_free_variables_in_ax_zero():
    a = np.array([[0, 2, 7, -1],
                  [-1, 2, 5, 5],
                  [-4, 13, 0, 6]])
    expected = 1
    actual = number_of_free_variables_in_ax_0(a)
    assert actual == expected


def test_arbitrary_partial_solution():
    a = np.array([[6, 1, -3, 5],
                  [2, 39, -17, 3],
                  [4, -9, 2, 3],
                  [-30, -5, 15, -25]])
    b = np.array([[1],
                  [-13],
                  [4],
                  [-5]])
    expected = np.array([13 / 58, -10 / 29, 0, 0])
    actual = arbitrary_partial_solution(a, b)
    assert np.isclose(actual, expected).all()


def test_diminsion_of_solution_set_ax_0():
    a = np.array([[1, -3, 1, -2, 9],
                  [0, 1, -3, -5, 4],
                  [-2, 7, -5, -1, -14],
                  [1, -5, 7, 8, 1]])
    expected = 3
    actual = diminsion_of_solution_set_ax_0(a)
    assert actual == expected


def test_n_vectors_in_basis_of_solution_set_in_ax_0():
    a = np.array([[4, 5, 7, -3, 1],
                  [11, 8, -4, 2, 0]])
    expected = 3
    actual = n_vectors_in_basis_of_solution_set_in_ax_zero(a)
    assert actual == expected
