from enp.linear_algebra import *


def n_vectors_in_basis_of_solution_set_in_ax_zero(a):
    """
    How many vectors are there in the basis of solution set for Ax=0?
    A basis is a fundamental system of solutions
    Not 100% sure the solution is correct. Check corner cases
    """
    return number_of_free_variables_in_ax_0(a)


def number_of_free_variables_in_ax_0(a):
    """
    How many free variables does the system Ax=0 have?
    Not 100% sure the solution is correct. Check corner cases
    """
    n = a.shape[1]
    rank_a = compute_rank(a)
    return n - rank_a


def diminsion_of_solution_set_ax_0(a):
    """
    What is the dimension of the solution set for Ax=0?
    Not sure in solution
    """
    n = a.shape[1]
    return n - compute_rank(a)


def arbitrary_partial_solution(a, b):
    """
    What is the x^0 (arbitrary partial solution) of Ax=b?
    Works only if there is infinite number of solutions
    """
    if b.ndim == 1:
        b = b[:, np.newaxis]
    if a.ndim != 2:
        raise ValueError
    if b.ndim != 2:
        raise ValueError

    if not does_system_of_linear_equations_has_solutions(a, b):
        raise ValueError

    a = a.astype('float32')
    b = b.astype('float32')
    ab = np.hstack((a, b))
    reduced_row_echelon_form = to_reduced_row_echelon_form(ab)

    n = a.shape[1]
    rank_ab = compute_rank(ab)
    n_free_variables = n - rank_ab
    # n_dependent_variables = n - n_free_variables
    if n_free_variables == 0:
        raise ValueError
    else:
        partial_solution = reduced_row_echelon_form[:, -1]
    return partial_solution
