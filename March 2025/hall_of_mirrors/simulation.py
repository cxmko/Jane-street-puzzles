import numpy as np

def simulate_ray(clue_side, clue_index, mirror_config, grid_size=10):
    """
    Simulates a ray's trajectory from a given starting position with the specified mirror configuration.
    
    Args:
        clue_side: The starting side ('top', 'right', 'bottom', 'left')
        clue_index: The starting index on the specified side
        mirror_config: The mirror configuration (list of (x, y, type) tuples)
        grid_size: Size of the grid (assuming square grid)
        
    Returns:
        A list of (x, y) cell coordinates representing the ray's path
    """
    # Determine starting position and direction based on the clue.
    if clue_side == "top":
        pos = (clue_index + 0.5, grid_size + 0.5)
        d = (0, -1)
    elif clue_side == "bottom":
        pos = (clue_index + 0.5, -0.5)
        d = (0, 1)
    elif clue_side == "left":
        pos = (-0.5, clue_index + 0.5)
        d = (1, 0)
    elif clue_side == "right":
        pos = (grid_size + 0.5, clue_index + 0.5)
        d = (-1, 0)
    else:
        return []
    
    ray_path = []
    # Continue simulation until the ray goes off the grid.
    while True:
        pos = (pos[0] + d[0], pos[1] + d[1])
        cell_x = int(pos[0] - 0.5)
        cell_y = int(pos[1] - 0.5)
        if not (0 <= cell_x < grid_size and 0 <= cell_y < grid_size):
            break
        ray_path.append((cell_x, cell_y))
        # Check if a mirror is present at this cell
        hit = None
        for (mx, my, mtype) in mirror_config:
            if mx == cell_x and my == cell_y:
                hit = mtype
                break
        if hit is not None:
            mirror_rules = {
                'A': {(0, 1): (1, 0), (1, 0): (0, 1), (0, -1): (-1, 0), (-1, 0): (0, -1)},
                'B': {(0, 1): (-1, 0), (-1, 0): (0, 1), (0, -1): (1, 0), (1, 0): (0, -1)}
            }
            d = mirror_rules[hit][d]
    return ray_path

def compute_trajectory_product(mat, side, idx, grid_size):
    """
    Compute the product of segment lengths for a ray trajectory.
    
    Args:
        mat: The grid matrix with mirrors encoded (-3 for A mirrors, -2 for B mirrors)
        side: The starting side ('top', 'right', 'bottom', 'left')
        idx: The starting index on the specified side
        grid_size: Size of the grid
        
    Returns:
        The product of all segment lengths in the trajectory
    """
    # Mirror reflection rules
    mirror_rules_A = {(0, 1):(1, 0), (1, 0):(0, 1), (0, -1):(-1, 0), (-1, 0):(0, -1)}
    mirror_rules_B = {(0, 1):(-1, 0), (-1, 0):(0, 1), (0, -1):(1, 0), (1, 0):(0, -1)}
    
    # Determine starting position and direction
    if side == "top":
        pos = (idx + 0.5, grid_size + 0.5)
        d = (0, -1)
    elif side == "bottom":
        pos = (idx + 0.5, -0.5)
        d = (0, 1)
    elif side == "left":
        pos = (-0.5, idx + 0.5)
        d = (1, 0)
    elif side == "right":
        pos = (grid_size + 0.5, idx + 0.5)
        d = (-1, 0)
    else:
        return 0

    product = 1

    while True:
        seg_length = 0
        # Advance in the current segment
        while True:
            # Compute new position
            new_pos = (pos[0] + d[0], pos[1] + d[1])
            # Convert new_pos to cell indices
            cell_x = int(new_pos[0] - 0.5)
            cell_y = int(new_pos[1] - 0.5)
            # Check if new_pos is in bounds
            if not (0 <= cell_x < grid_size and 0 <= cell_y < grid_size):
                break  # Out-of-bounds: segment ends
            # Check if the new cell contains a mirror
            if mat[cell_y, cell_x] in (-2, -3):
                break  # Hit a mirror: segment ends
            # Otherwise, accept the step
            pos = new_pos
            seg_length += 1
        # End of segment; multiply product
        product *= (seg_length + 1)
        # Now, check why we stopped
        new_pos = (pos[0] + d[0], pos[1] + d[1])
        cell_x = int(new_pos[0] - 0.5)
        cell_y = int(new_pos[1] - 0.5)
        # If out-of-bounds, we are done
        if not (0 <= cell_x < grid_size and 0 <= cell_y < grid_size):
            break
        # Otherwise, we hit a mirror; determine its type
        mirror_val = mat[cell_y, cell_x]
        # Reflect the ray accordingly
        if mirror_val == -3:  # Mirror type A
            d = mirror_rules_A[d]
        elif mirror_val == -2:  # Mirror type B
            d = mirror_rules_B[d]
        # Set pos to the mirror cell (starting new segment from there)
        pos = new_pos
    
    return product
