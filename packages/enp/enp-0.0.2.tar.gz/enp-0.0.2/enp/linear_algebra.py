from enp.linear_algebra_utils import *


def transpose_2d(x):
    if x.ndim != 2:
        raise ValueError
    x = x.astype(np.float32)
    if not len(x.shape) == 2:
        raise ValueError
    x_t = np.zeros((x.shape[1], x.shape[0]), dtype='float32')
    for i in range(x.shape[0]):
        for j in range(x.shape[1]):
            x_t[j, i] = x[i, j]
    return x_t


def matrix_sum_2d(x, y):
    if not x.shape == y.shape:
        raise ValueError
    x = x.astype(np.float32)
    y = y.astype(np.float32)
    output = np.zeros(x.shape, dtype='float32')
    for i in range(x.shape[0]):
        for j in range(x.shape[1]):
            output[i][j] = x[i][j] + y[i][j]
    return output


def matrix_mult_2d(x, y):
    if x.shape[1] != y.shape[0]:
        raise ValueError
    if x.ndim != 2:
        raise ValueError
    if y.ndim != 2:
        raise ValueError
    x = x.astype(np.float32)
    y = y.astype(np.float32)
    output = np.zeros((x.shape[0], y.shape[1]))
    for i in range(x.shape[0]):
        for j in range(y.shape[1]):
            for k in range(x.shape[1]):
                output[i, j] += x[i, k] * y[k, j]
    return output


def solve_system_of_linear_equations(a, b):
    """
    TODO check corner cases
    """
    if b.ndim == 1:
        b = b[:, np.newaxis]
    if a.ndim != 2:
        raise ValueError
    if b.ndim != 2:
        raise ValueError

    if not does_system_of_linear_equations_has_solutions(a, b):
        print('No solutions')
        return

    a = a.astype('float32')
    b = b.astype('float32')
    ab = np.hstack((a, b))
    reduced_row_echelon_form = to_reduced_row_echelon_form(ab)

    n = a.shape[1]
    rank_ab = compute_rank(ab)
    n_free_variables = n - rank_ab
    n_dependent_variables = n - n_free_variables
    if n_free_variables == 0:
        return reduced_row_echelon_form[:, -1]
    else:
        partial = reduced_row_echelon_form[:, -1]
        print(f"x = {partial}^T")
        homogeneous = []
        for i in range(n_dependent_variables, n):
            variable = f'x_{i + 1}'
            vector = -1 * reduced_row_echelon_form[:, i]
            print(f"+ {variable} {vector}^T")


def to_reduced_row_echelon_form(x):
    if x.ndim != 2:
        raise ValueError
    x = x.astype(np.float32)
    lead = 0
    row_count = x.shape[0]
    column_count = x.shape[1]
    for r in range(row_count):
        if column_count <= lead:
            return x
        i = r
        while x[i, lead] == 0:
            i += 1
            if row_count == i:
                i = r
                lead += 1
                if column_count == lead:
                    return x
        if i != r:
            x[[i, r]] = x[[r, i]]
        x[r, :] = x[r, :] / x[r, lead]
        for i in range(row_count):
            if i != r:
                x[i, :] = x[i, :] - x[i, lead] * x[r, :]
                x = aproximately_zero_to_zero(x)
        lead += 1
    return x


def inverse_2d(x):
    if x.ndim != 2:
        raise ValueError
    if x.shape[0] != x.shape[1]:
        raise ValueError
    n = x.shape[0]
    identity = np.eye(n)
    x = np.hstack((x, identity))
    x = to_reduced_row_echelon_form(x)
    output = x[:, -n:]
    if np.all(x[:, :n] == np.eye(n)):
        return output
    else:
        raise ValueError


def compute_rank(x):
    if x.ndim != 2:
        raise ValueError
    x = x.astype(np.float32)
    x = to_reduced_row_echelon_form(x)
    rank = x.shape[0]
    for r in reversed(range(x.shape[0])):
        if np.all(x[r, :] == 0):
            rank -= 1
        else:
            return rank
    return rank


def rank_factorization(a):
    b = to_reduced_row_echelon_form(a)
    pivot_columns = []
    for r in range(b.shape[0]):
        for c in range(b.shape[1]):
            if b[r, c] != 0:
                pivot_columns.append(c)
                break
    c = a[:, pivot_columns]
    non_zero_rows_of_b = []
    for r in range(b.shape[0]):
        if np.any(b[r, :] != 0):
            non_zero_rows_of_b.append(r)
    f = b[non_zero_rows_of_b, :]
    return c, f


def does_system_of_linear_equations_has_solutions(a, b):
    """
    Rouché–Capelli theorem:
    System of linear equations Ax=b has solutions iff rank(A) = rank(A|b)
    """
    if b.ndim == 1:
        b = b[:, np.newaxis]
    if a.ndim != 2:
        raise ValueError
    if b.ndim != 2:
        raise ValueError
    a = a.astype('float32')
    b = b.astype('float32')
    ab = np.hstack((a, b))

    rank_a = compute_rank(a)
    rank_ab = compute_rank(ab)
    return rank_a == rank_ab


def dot_product_1d(a, b):
    a = a.astype(np.float32)
    b = b.astype(np.float32)
    if a.shape != b.shape:
        raise ValueError
    if a.ndim != 1:
        raise ValueError
    return np.sum(np.multiply(a, b))


def length_of_vector(x):
    return np.sqrt(dot_product_1d(x, x))


def angle_between_vectors(x, y):
    return np.arccos(dot_product_1d(x, y) / (length_of_vector(x) * length_of_vector(y)))


def least_squares_ax_b(a, b):
    """
    Find the approximation to the solution of Ax=b using least squares method
    TODO test it
    """
    if b.ndim == 1:
        b = b[:, np.newaxis]
    if a.ndim != 2:
        raise ValueError
    if b.ndim != 2:
        raise ValueError
    a = a.astype('float32')
    b = b.astype('float32')
    return np.linalg.inv(a.T @ a) @ a.T @ b
