import numpy as np

def is_valid_path(factors, side, index, grid_size, clue_num, cluepos, start_pos=None, 
                 direction=None, mirrors=None, trajectory=None, top_level=True):
    """
    Checks if a path with the given factorization, starting side and index is valid 
    within the grid constraints.
    
    Args:
        factors: Tuple of integers representing segment lengths
        side: Starting side ('top', 'right', 'bottom', 'left')
        index: Starting index on the specified side
        grid_size: Size of the grid (assuming square grid)
        clue_num: The clue number to check against
        cluepos: Dictionary mapping positions to clue numbers
        start_pos: Starting position (for recursive calls)
        direction: Starting direction (for recursive calls)
        mirrors: List of placed mirrors (for recursive calls)
        trajectory: List of cells in the ray's path (for recursive calls)
        top_level: Whether this is the top-level call (vs. recursive)
        
    Returns:
        If top_level is True:
            A tuple of (mirror_configs, matrix_list) where:
            - mirror_configs is a list of valid mirror configurations
            - matrix_list is a list of (matrix, index) tuples
        Otherwise:
            A list of valid mirror configurations
    """
    def maybe_convert(result):
        if top_level:
            mirror_configs = [sol[0] for sol in result]
            matrix_list = [(sol[1], idx) for idx, sol in enumerate(result)]
            return mirror_configs, matrix_list
        else:
            return result
    
    if start_pos is None or direction is None or mirrors is None or trajectory is None:
        # Initialize starting position and direction based on the chosen side.
        if side == 'top':
            x = index + 0.5
            y = grid_size + 0.5
            dx, dy = 0, -1
        elif side == 'right':
            x = grid_size + 0.5
            y = index + 0.5
            dx, dy = -1, 0
        elif side == 'bottom':
            x = index + 0.5
            y = -0.5
            dx, dy = 0, 1
        elif side == 'left':
            x = -0.5
            y = index + 0.5
            dx, dy = 1, 0
        start_pos = (x, y)
        direction = (dx, dy)
        mirrors = []
        trajectory = [] 
    
    x, y = start_pos
    dx, dy = direction
    current_mirrors = mirrors.copy()
    current_trajectory = trajectory.copy()
    
    # Mirror reflection rules for types A and B.
    mirror_rules = {
        'A': {(0, 1): (1, 0), (1, 0): (0, 1), (0, -1): (-1, 0), (-1, 0): (0, -1)},
        'B': {(0, 1): (-1, 0), (-1, 0): (0, 1), (0, -1): (1, 0), (1, 0): (0, -1)}
    }
    
    try:
        for i, length in enumerate(factors):
            # Compute the endpoint for this segment.
            end_x = x + dx * length
            end_y = y + dy * length
            
            # Compute the cells along this segment.
            segment_cells = []
            # Each step from 1 to length (inclusive)
            for step in range(1, length + 1):
                pos_x = x + dx * step
                pos_y = y + dy * step
                # Convert center coordinate (e.g., 0.5, 1.5, etc.) to cell indices.
                cell_x = int(pos_x - 0.5)
                cell_y = int(pos_y - 0.5)
                # Only add if inside grid bounds.
                if 0 <= cell_x < grid_size and 0 <= cell_y < grid_size:
                    segment_cells.append((cell_x, cell_y))
            
            # Update the trajectory with the new segment's cells.
            new_trajectory = current_trajectory + segment_cells

            # Non-final segments must end at a valid mirror location.
            if i < len(factors) - 1:
                # Ensure the end position is at a cell center (ends with .5).
                if not (end_x % 1 == 0.5 and end_y % 1 == 0.5):
                    return []
                
                cell_x = int(end_x - 0.5)
                cell_y = int(end_y - 0.5)
                
                # Check that the mirror cell is within grid bounds.
                if not (0 <= cell_x < grid_size and 0 <= cell_y < grid_size):
                    return []
                
                # Ensure there are no adjacent mirrors.
                for (mx, my, _) in current_mirrors:
                    if abs(mx - cell_x) + abs(my - cell_y) == 1:
                        return []
                
                solutions = []
                # Try both mirror types.
                for mt in ['A', 'B']:
                    new_dx, new_dy = mirror_rules[mt][(dx, dy)]
                    new_start = (end_x, end_y)
                    new_direction = (new_dx, new_dy)
                    sols = is_valid_path(
                        factors[i+1:],
                        side,
                        index,
                        grid_size,
                        clue_num,
                        cluepos,
                        new_start,
                        new_direction,
                        current_mirrors + [(cell_x, cell_y, mt)],
                        new_trajectory,
                        top_level=False,
                    )
                    solutions.extend(sols)
                
                if solutions:
                    return maybe_convert(solutions)
                else:
                    return maybe_convert([])
            
            # Final segment: check if the segment exits the grid.
            else:
                exit_clash = ((end_x, end_y) in cluepos) and cluepos[(end_x, end_y)] != clue_num
                # For the final segment, if the endpoint is out of grid bounds, the path is valid.
                if (end_x == -0.5 or end_x == grid_size + 0.5 or
                    end_y == -0.5 or end_y == grid_size + 0.5) and not exit_clash:
                    final_trajectory = new_trajectory
                    # Create the NumPy matrix.
                    mat = np.zeros((grid_size, grid_size), dtype=int)
                    # Mark the trajectory cells with 1's.
                    for (cx, cy) in final_trajectory:
                        mat[cy, cx] = 1
                    # Overwrite mirror positions: A -> -3, B -> -2.
                    for (mx, my, mtype) in current_mirrors:
                        if mtype == 'A':
                            mat[my, mx] = -3
                        elif mtype == 'B':
                            mat[my, mx] = -2
                        # Mark adjacent orthogonal cells with -4.
                        for (adj_x, adj_y) in [(mx+1, my), (mx-1, my), (mx, my+1), (mx, my-1)]:
                            if 0 <= adj_x < grid_size and 0 <= adj_y < grid_size:
                                mat[adj_y, adj_x] = -4
                    return maybe_convert([(current_mirrors, mat)])
                else:
                    return maybe_convert([])
        
        return maybe_convert([])
    
    except KeyError:
        return maybe_convert([])
