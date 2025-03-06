import numpy as np
import matplotlib.pyplot as plt
from .simulation import compute_trajectory_product

def plot_solution(mirrors, grid_size=10, trajectory_products=None):
    """
    Create a visualization of the puzzle solution.
    
    Args:
        mirrors: List of (x, y, type) tuples representing mirror placements
        grid_size: Size of the grid (square)
        trajectory_products: Optional pre-calculated trajectory products for border cells
        
    Returns:
        The matplotlib figure showing the solution
    """
    # If not provided, calculate trajectory products
    if trajectory_products is None:
        # Create the matrix with mirror placements
        final_matrix = np.zeros((grid_size, grid_size), dtype=int)
        for (col, row, mtype) in mirrors:
            if mtype == "A":
                final_matrix[row, col] = -3
            elif mtype == "B":
                final_matrix[row, col] = -2
        
        # Calculate trajectory products for each border cell
        trajectory_products = {}
        for side in ["top", "bottom", "left", "right"]:
            for idx in range(grid_size):
                prod = compute_trajectory_product(final_matrix, side, idx, grid_size)
                trajectory_products[(side, idx)] = prod
    
    # Setup the plot
    fig, ax = plt.subplots(figsize=(8, 8))
    # Expand axis limits to show dots outside the grid
    offset_text = 0.3
    dot_offset = 0.2
    ax.set_xlim(0 - dot_offset - 0.5, grid_size + dot_offset + 0.5)
    ax.set_ylim(0 - dot_offset - 0.5, grid_size + dot_offset + 0.5)
    ax.set_aspect('equal')

    # Draw grid lines
    for x in range(grid_size + 1):
        ax.plot([x, x], [0, grid_size], color='black', lw=1)
    for y in range(grid_size + 1):
        ax.plot([0, grid_size], [y, y], color='black', lw=1)

    # Draw mirror markers
    for (col, row, mtype) in mirrors:
        if mtype == "A":
            ax.plot([col, col+1], [row, row+1], color='red', lw=3)
        elif mtype == "B":
            ax.plot([col, col+1], [row+1, row], color='red', lw=3)

    # Get the trajectory products for each side
    top_numbers = [trajectory_products[("top", i)] for i in range(grid_size)]
    bottom_numbers = [trajectory_products[("bottom", i)] for i in range(grid_size)]
    left_numbers = [trajectory_products[("left", i)] for i in range(grid_size)]
    right_numbers = [trajectory_products[("right", i)] for i in range(grid_size)]

    # Annotate borders with numbers and dots
    # Top border
    for i, num in enumerate(top_numbers):
        x = i + 0.5
        ax.text(x, grid_size + offset_text, str(num),
                ha='center', va='bottom', fontsize=14, fontweight='bold')
        ax.scatter(x, grid_size + dot_offset, s=20, color='black', marker='o')

    # Bottom border
    for i, num in enumerate(bottom_numbers):
        x = i + 0.5
        ax.text(x, -offset_text, str(num),
                ha='center', va='top', fontsize=14, fontweight='bold')
        ax.scatter(x, 0 - dot_offset, s=20, color='black', marker='o')

    # Left border
    for i, num in enumerate(left_numbers):
        y = i + 0.5
        ax.text(-offset_text, y, str(num),
                ha='right', va='center', fontsize=14, fontweight='bold')
        ax.scatter(0 - dot_offset, y, s=20, color='black', marker='o')

    # Right border
    for i, num in enumerate(right_numbers):
        y = i + 0.5
        ax.text(grid_size + offset_text, y, str(num),
                ha='left', va='center', fontsize=14, fontweight='bold')
        ax.scatter(grid_size + dot_offset, y, s=20, color='black', marker='o')

    # Hide the axes
    ax.axis('off')
    
    return fig
