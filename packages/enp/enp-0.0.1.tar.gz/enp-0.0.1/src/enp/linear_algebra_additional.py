import numpy as np
from src.enp.linear_algebra import *
from src.enp.linear_algebra_utils import *


def n_vectors_in_basis_of_solution_set(A):
    """
    How many vectors are there in the basis of solution set for Ax=0.
    A basis is a fundamental system of solutions
    TODO
    """
    pass


def number_of_free_variables(A):
    """
    How many free variables does the system Ax=0 have
    TODO
    """


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



