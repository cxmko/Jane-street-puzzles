"""
Hall of Mirrors - A ray tracing puzzle solver

This package provides tools for solving Hall of Mirrors puzzles, which involve 
placing mirrors to create specific ray trajectories.
"""

from .factorization import ultra_factorizations
from .path_validation import is_valid_path
from .simulation import simulate_ray, compute_trajectory_product
from .visualization import plot_solution
from .solver import solve_puzzle, produce_matrix, is_compatible, merge_layers

__all__ = [
    'ultra_factorizations',
    'is_valid_path',
    'simulate_ray',
    'compute_trajectory_product',
    'plot_solution',
    'solve_puzzle',
    'produce_matrix',
    'is_compatible',
    'merge_layers'
]
