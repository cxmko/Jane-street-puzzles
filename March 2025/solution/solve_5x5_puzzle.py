"""
Example script demonstrating how to solve a Hall of Mirrors puzzle
"""
import sys
import os
# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
from hall_of_mirrors.visualization import plot_solution
from hall_of_mirrors.solver import solve_puzzle
import matplotlib.pyplot as plt

def main():
    # Define puzzle parameters
    grid_size = 5
    
    # Define the clue numbers
    numbers = [9, 16, 75, 36]
    
    # Map clue numbers to their positions (side and index)
    dic = {
        9: ["top", 2], 
        16: ["left", 1], 
        75: ["right", 3], 
        36: ["bottom", 2]
    }
    
    # Map positions to clue numbers
    cluepos = {
        (2.5, 5.5): 9,
        (-0.5, 1.5): 16, 
        (5.5, 3.5): 75, 
        (2.5, -0.5): 36
    }
    
    # Solve the puzzle
    print("Solving the puzzle...")
    solution = solve_puzzle(
        numbers=numbers,
        cluepos=cluepos,
        dic=dic,
        max_tuple_length=25//2,  # Maximum factorization length
        max_factor=6,            # Maximum factor value
        grid_size=grid_size      # Grid size
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
            "top": [dic[n][1] for n in numbers if dic[n][0] == "top"],
            "bottom": [dic[n][1] for n in numbers if dic[n][0] == "bottom"],
            "left": [dic[n][1] for n in numbers if dic[n][0] == "left"],
            "right": [dic[n][1] for n in numbers if dic[n][0] == "right"],
        }
        
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
