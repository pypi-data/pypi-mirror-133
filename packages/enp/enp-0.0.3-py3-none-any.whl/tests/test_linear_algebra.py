import pytest
from sympy import Matrix
from enp.linear_algebra import *


def test_transpose2d():
    x = np.array([[0, -2, 7],
                  [12, 3, 8],
                  [-4, 9, 0],
                  [7, 6, -1]])
    expected = np.array([[0, 12, -4, 7],
                         [-2, 3, 9, 6],
                         [7, 8, 0, -1]])
    actual = transpose_2d(x)
    assert np.isclose(actual, expected).all()

    x = np.array([[4, 1, 0],
                  [-3, 1, 4],
                  [15, -9, 1],
                  [11, 2, 3],
                  [5, -3, 3]])
    expected = np.array([[4, -3, 15, 11, 5],
                         [1, 1, -9, 2, -3],
                         [0, 4, 1, 3, 3]])
    actual = transpose_2d(x)
    assert np.isclose(actual, expected).all()


def test_matrix_sum_2d():
    x = np.array([[1, 2, 3],
                  [4, 5, 6]])
    y = np.array([[7, 8, 9],
                  [10, 11, 12]])
    actual = matrix_sum_2d(x, y)
    expected = x + y
    assert np.isclose(actual, expected).all()

    x = np.array([[0, 4, -7, 12]])
    y = np.array([[13, 5, 15, 8]])
    actual = matrix_sum_2d(x, y)
    expected = np.array([[13, 9, 8, 20]])
    assert np.isclose(actual, expected).all()


def test_matrix_mult_2d():
    x = np.array([[1, 2, 3],
                  [4, 5, 6]])
    y = np.array([[7, 8],
                  [9, 10],
                  [11, 12]])
    actual = matrix_mult_2d(x, y)
    expected = x @ y
    assert np.isclose(actual, expected).all()

    x = np.array([[1, -4, 15],
                  [9, -6, 13]])
    y = np.array([[4, 3],
                  [-3, 0],
                  [5, 1],
                  [0, 7]])
    with pytest.raises(Exception):
        matrix_mult_2d(x, y)

    x = np.array([[0, 9, -3, 6]])
    y = np.array([[4],
                  [-3],
                  [5],
                  [0]])
    actual = matrix_mult_2d(x, y)
    expected = np.array([[-42]])
    assert np.isclose(actual, expected).all()


def test_solve_system_of_linear_equations():
    a = np.array([[0, -2],
                  [4, 7]])
    b = np.array([[1],
                  [2]])
    expected = np.array([11 / 8, -1 / 2])
    actual = solve_system_of_linear_equations(a, b)
    assert np.isclose(actual, expected).all()

    a = np.array([[3, 1],
                  [2, -5]])
    b = np.array([2, 1])
    expected = np.array([33 / 51, 1 / 17])
    actual = solve_system_of_linear_equations(a, b)
    assert np.isclose(actual, expected).all()

    a = np.array([[1, -2, 3],
                  [-3, 0, 2],
                  [1, -1, 4]])
    b = np.array([5, 2, 6])
    expected = np.array([4 / 17, -6 / 17, 23 / 17])
    actual = solve_system_of_linear_equations(a, b)
    assert np.isclose(actual, expected).all()

    a = np.array([[1, 2], [3, 5]])
    b = np.array([1, 2])
    expected = np.linalg.solve(a, b)
    actual = solve_system_of_linear_equations(a, b)
    assert np.isclose(actual, expected).all()


def test_to_reduced_row_echelon_form():
    x_python = [[1, 3, -1], [0, 1, 7]]
    # x_sympy = Matrix(x_python)
    # expected = np.array(x_sympy.rref()[0]).astype(np.float32)
    expected = np.array([[1, 0, -22],
                         [0, 1, 7]])
    x_numpy = np.array(x_python)
    actual = to_reduced_row_echelon_form(x_numpy)
    assert np.isclose(actual, expected).all()

    x_python = [[1, 0, 1, 3], [2, 3, 4, 7], [-1, -3, -3, -4]]
    x_sympy = Matrix(x_python)
    expected = np.array(x_sympy.rref()[0]).astype(np.float32)
    x_numpy = np.array(x_python)
    actual = to_reduced_row_echelon_form(x_numpy)
    assert np.isclose(actual, expected).all()


def test_inverse_2d():
    x = np.array([[3, 5, -1],
                  [-4, 1, 2],
                  [0, 1, 0]])
    expected = np.array([[1, 0.5, -5.5],
                         [0, 0, 1],
                         [2, 1.5, -11.5]])
    actual = inverse_2d(x)
    assert np.isclose(actual, expected).all()

    x = np.array([[0, 5, 1],
                  [-2, 1, -4],
                  [1, 6, 0]])
    expected = np.array([[-8 / 11, -2 / 11, 7 / 11],
                         [4 / 33, 1 / 33, 2 / 33],
                         [13 / 33, -5 / 33, -10 / 33]])
    actual = inverse_2d(x)
    assert np.isclose(actual, expected).all()


def test_compute_rank():
    x = np.array([[1, 4, 5],
                  [-5, 8, 9],
                  [-12, 8, 8]])
    expected = 2
    expected_external = np.linalg.matrix_rank(x)
    actual = compute_rank(x)
    assert actual == expected_external
    assert actual == expected

    x = np.array([[3, -1, 1, 9],
                  [-3, 4, 1, 1],
                  [6, 5, 2, 8],
                  [1, 1, 1, 1]])
    expected = 4
    expected_external = np.linalg.matrix_rank(x)
    actual = compute_rank(x)
    assert actual == expected_external
    assert actual == expected


def test_rank_factorization():
    a = np.array([[1, 3, 1, 4],
                  [2, 7, 3, 9],
                  [1, 5, 3, 1],
                  [1, 2, 0, 8]])
    c_expected = np.array([[1, 3, 4],
                           [2, 7, 9],
                           [1, 5, 1],
                           [1, 2, 8]])
    f_expected = np.array([[1, 0, -2, 0],
                           [0, 1, 1, 0],
                           [0, 0, 0, 1]])
    c_actual, f_actual = rank_factorization(a)
    a_actual = np.matmul(c_actual, f_actual)
    assert np.isclose(c_actual, c_expected).all()
    assert np.isclose(f_actual, f_expected).all()
    assert np.isclose(a_actual, a).all()

    a = np.array([[3, 2, 1, -1],
                  [-1, -2, 1, 2],
                  [1, -2, 3, 3]])
    c_expected = np.array([[3, 2],
                           [-1, -2],
                           [1, -2]])
    f_expected = np.array([[1, 0, 1, 1 / 2],
                           [0, 1, -1, -5 / 4]])
    c_actual, f_actual = rank_factorization(a)
    a_actual = np.matmul(c_actual, f_actual)
    assert np.isclose(c_actual, c_expected).all()
    assert np.isclose(f_actual, f_expected).all()
    assert np.isclose(a_actual, a).all()

    a = np.array([[1, 1, 1],
                  [2, 2, 2],
                  [3, 3, 3],
                  [1, 2, 3]])
    c_expected = np.array([[1, 1],
                           [2, 2],
                           [3, 3],
                           [1, 2]])
    f_expected = np.array([[1, 0, -1],
                           [0, 1, 2]])
    c_actual, f_actual = rank_factorization(a)
    a_actual = np.matmul(c_actual, f_actual)
    assert np.isclose(c_actual, c_expected).all()
    assert np.isclose(f_actual, f_expected).all()
    assert np.isclose(a_actual, a).all()


def test_does_system_of_linear_equations_has_solutions():
    a = np.array([[4, 1, -8, 5],
                  [-3, 1, 4, 7],
                  [1, 2, -4, 12],
                  [1, 1, 1, 1]])
    b = np.array([2, 1, 1, 1])
    expected = False
    actual = does_system_of_linear_equations_has_solutions(a, b)
    assert actual == expected

    a = np.array([[-8, -1, 5],
                  [-5, 2, 7],
                  [0, 3, 8]])
    b = np.array([1, 0, 2])
    expected = True
    actual = does_system_of_linear_equations_has_solutions(a, b)
    assert actual == expected


def test_dot_product_1d():
    a = np.array([-1, 1, 2, 3])
    b = np.array([0, 1, -5, 16])
    expected = 39
    expected_external = np.dot(a, b)
    actual = dot_product_1d(a, b)
    assert np.isclose(actual, expected)
    assert np.isclose(actual, expected_external)


def test_length_of_vector():
    x = np.array([1, -7, 3])
    expected = np.sqrt(59)
    expected_external = np.linalg.norm(x)
    actual = length_of_vector(x)
    assert np.isclose(actual, expected)
    assert np.isclose(actual, expected_external)


def test_angle_between_vectors():
    x = np.array([1, -3, 0])
    y = np.array([0, 1, -7])
    expected = np.arccos(-3 / (10 * np.sqrt(5)))
    actual = angle_between_vectors(x, y)
    assert np.isclose(actual, expected)


def test_least_squares_ax_b():
    a = np.array([[3, -5],
                  [1, -7],
                  [0, 1]])
    b = np.array([[0],
                  [2],
                  [5]])
    actual = least_squares_ax_b(a, b)
    expected = np.array([[-24 / 133],
                         [-23 / 133]])
    assert np.all(np.isclose(actual, expected))


def test_orthogonal_projection_of_x_onto_l():
    a = np.array([[1, 0],
                  [0, -1],
                  [1, 1]])
    x = np.array([[1],
                  [1],
                  [2]])
    actual = orthogonal_projection_of_x_onto_l(a, x)
    expected = np.array([[5 / 3],
                         [1 / 3],
                         [4 / 3]])
    assert np.all(np.isclose(actual, expected))


def test_change_basis():
    a = np.array([[1, -2],
                  [2, 3]])
    b = np.array([[-1, 1],
                  [2, 1]])
    x_a = np.array([[3],
                    [-1]])
    actual = change_basis(a, b, x_a)
    expected = np.array([[-2 / 3],
                         [13 / 3]])
    assert np.all(np.isclose(actual, expected))


def test_distance_from_point_to_plane():
    point = [0, 3, 6]
    plane_parameters = [2, 4, -4, 6]
    actual = distance_from_point_to_plane(point, plane_parameters)
    expected = 3
    assert np.isclose(actual, expected)


def test_distance_from_point_to_hyperplane():
    # See the same example in test_distance_from_point_to_plane
    y = [0, 3, 6]
    a = [2, 4, -4]
    d = 6
    actual = distance_from_point_to_hyperplane(y, a, d)
    expected = 3
    assert np.isclose(actual, expected)


def test_distance_from_point_to_line():
    point = [3, -4]
    line_parameters = [6, -8, -5]
    actual = distance_from_point_to_line(point, line_parameters)
    expected = 4.5
    assert np.isclose(actual, expected)


def test_distance_between_two_parallel_lines():
    line_parameters_1 = [5, 3, 6]
    line_parameters_2 = [5, 3, -6]
    actual = distance_between_two_parallel_lines(line_parameters_1, line_parameters_2)
    expected = 12 / np.sqrt(34)
    assert np.isclose(actual, expected)
