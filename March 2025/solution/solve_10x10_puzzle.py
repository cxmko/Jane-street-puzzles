"""
Script solving the 10x10 Hall of Mirrors puzzle with the specified clues
"""
import sys
import os
# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import matplotlib.pyplot as plt

# Import functionality from the hall_of_mirrors package instead of redefining
from hall_of_mirrors.factorization import ultra_factorizations
from hall_of_mirrors.path_validation import is_valid_path
from hall_of_mirrors.simulation import simulate_ray, compute_trajectory_product
from hall_of_mirrors.visualization import plot_solution
from hall_of_mirrors.solver import solve_puzzle

def main():
    # Define puzzle parameters
    grid_size = 10
    
    # Define the entries as tuples (clue_number, [side, index])
    entries = [
        (112, ["top", 2]), 
        (48, ["top", 4]), 
        (3087, ["top", 5]), 
        (9, ["top", 6]), 
        (1, ["top", 9]),
        (27, ["left", 6]), 
        (12, ["left", 2]), 
        (225, ["left", 1]),
        (2025, ["bottom", 0]), 
        (12, ["bottom", 3]), 
        (64, ["bottom", 4]), 
        (5, ["bottom", 5]), 
        (405, ["bottom", 7]),
        (4, ["right", 8]), 
        (27, ["right", 7]), 
        (16, ["right", 3])
    ]
    
    # Map positions to clue numbers
    cluepos = {
        (2.5, 10.5): 112, 
        (4.5, 10.5): 48, 
        (5.5, 10.5): 3087, 
        (6.5, 10.5): 9, 
        (9.5, 10.5): 1,
        (-0.5, 6.5): 27, 
        (-0.5, 2.5): 12, 
        (-0.5, 1.5): 225,
        (0.5, -0.5): 2025, 
        (3.5, -0.5): 12, 
        (4.5, -0.5): 64, 
        (5.5, -0.5): 5, 
        (7.5, -0.5): 405,
        (10.5, 8.5): 4, 
        (10.5, 7.5): 27, 
        (10.5, 3.5): 16
    }
    
    # Extract clue numbers for solve_puzzle 
    numbers = [entry[0] for entry in entries]
    
    # Create dictionary mapping clue numbers to [side, index]
    dic = {number: info for number, info in entries}
    
    # Solve the puzzle
    print("Solving the 10x10 Hall of Mirrors puzzle...")
    solution = solve_puzzle(
        numbers=numbers,
        cluepos=cluepos,
        dic=dic,
        max_tuple_length=50,  # Maximum factorization length
        max_factor=11,        # Maximum factor value
        grid_size=grid_size   # Grid size
    )
    
    if solution:
        mirror_configs, final_matrix, trajectory_products = solution
        
        # Print solutions
        print("\nSolution found!")
        print("\nMirror configurations:")
        for i, config in enumerate(mirror_configs):
            print(f"Clue {numbers[i]}: {config}")
        
        # Get all mirrors from the configurations
        all_mirrors = []
        for config in mirror_configs:
            for mirror in config:
                if mirror not in all_mirrors:
                    all_mirrors.append(mirror)
        
        # Visualize the solution
        print("\nPlotting solution...")
        fig = plot_solution(all_mirrors, grid_size, trajectory_products)
        plt.show()
        
        # Calculate the unique bordered cell values
        print("\nCalculating border values...")
        valid_indices = {
            "top": [],
            "bottom": [],
            "left": [],
            "right": []
        }
        
        # Fill valid indices from entries
        for number, [side, idx] in entries:
            valid_indices[side].append(idx)
        
        sums = {}
        for side in ["top", "bottom", "left", "right"]:
            # Sum the values from positions that aren't part of the clue positions
            sums[side] = sum(
                trajectory_products[(side, i)] 
                for i in range(grid_size) 
                if i not in valid_indices[side]
            )
            print(f"Sum of {side} border values (non-clue positions): {sums[side]}")
        
        print(f"\nProduct of all sums: {sums['top'] * sums['bottom'] * sums['left'] * sums['right']}")
        
    else:
        print("No solution found!")

if __name__ == "__main__":
    main()
