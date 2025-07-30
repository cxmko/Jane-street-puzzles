import numpy as np
from .factorization import ultra_factorizations
from .path_validation import is_valid_path
from .simulation import simulate_ray, compute_trajectory_product

def produce_matrix(config, clue_num, clue_info, grid_size=10):
    """
    Given a mirror configuration and a clue, produce a candidate matrix.
    
    Args:
        config: Mirror configuration (list of (x, y, type) tuples)
        clue_num: Clue number
        clue_info: Information about the clue (side, index)
        grid_size: Size of the grid
        
    Returns:
        A numpy matrix with the mirror configuration and ray path
    """
    mat = np.zeros((grid_size, grid_size), dtype=int)
    # Place mirrors and adjacent -4's
    for (mx, my, mtype) in config:
        if mtype == 'A':
            mat[my, mx] = -3
        elif mtype == 'B':
            mat[my, mx] = -2
        for (adj_x, adj_y) in [(mx+1, my), (mx-1, my), (mx, my+1), (mx, my-1)]:
            if 0 <= adj_x < grid_size and 0 <= adj_y < grid_size:
                mat[adj_y, adj_x] = -4
    
    # Simulate ray and mark path
    ray_path = simulate_ray(clue_info[0], clue_info[1], config, grid_size)
    for (rx, ry) in ray_path:
        if mat[ry, rx] == 0:
            mat[ry, rx] = 1
    
    return mat

def is_compatible(base, cand):
    """
    Check if a candidate matrix is compatible with a base matrix.
    
    Args:
        base: Base matrix
        cand: Candidate matrix
        
    Returns:
        True if compatible, False otherwise
    """
    for i in range(base.shape[0]):
        for j in range(base.shape[1]):
            M = base[i, j]
            L = cand[i, j]
            if L == 0:
                continue
            if L == 1:
                if M in {-2, -3}:
                    return False
            elif L in {-2, -3}:
                if M in {-4, 1}:
                    return False
                if M in {-2, -3} and M != L:
                    return False
            elif L == -4:
                if M in {-2, -3}:
                    return False
    return True

def merge_layers(base, cand):
    """
    Merge a candidate layer onto a base matrix.
    
    Args:
        base: Base matrix
        cand: Candidate matrix
        
    Returns:
        The merged matrix
    """
    new = base.copy()
    for i in range(new.shape[0]):
        for j in range(new.shape[1]):
            if cand[i, j] != 0 and new[i, j] == 0:
                new[i, j] = cand[i, j]
            elif cand[i, j] == -4:
                new[i, j] = -4
    return new

def solve_puzzle(numbers, cluepos, dic, max_tuple_length, max_factor, grid_size=10):
    """
    Solve the Hall of Mirrors puzzle.
    
    Args:
        numbers: List of clue numbers
        cluepos: Dictionary mapping positions to clue numbers
        dic: Dictionary mapping clue numbers to (side, index)
        max_tuple_length: Maximum factorization tuple length
        max_factor: Maximum allowed factor
        grid_size: Size of the grid
        
    Returns:
        A tuple containing:
        - The list of mirror configurations
        - The final merged matrix
        - A dictionary of trajectory products
    """
    # Generate factorizations for all numbers
    result = ultra_factorizations(numbers, max_tuple_length, max_factor)
    
    # Find valid paths for each factorization
    valid_configs = [[] for _ in range(len(numbers))]
    for i in range(len(result)):
        for factors in result[i]:
            clue_num = numbers[i]
            clue_side, clue_idx = dic[clue_num]
            paths = is_valid_path(factors, clue_side, clue_idx, grid_size, 
                                 clue_num, cluepos)
            if paths:
                valid_configs[i].extend(paths[0])
    
    # Create candidate layers
    candidate_layers = []
    for i in range(len(numbers)):
        clue_num = numbers[i]
        candidates = []
        for config in valid_configs[i]:
            mat = produce_matrix(config, clue_num, dic[clue_num], grid_size)
            candidates.append((config, mat))
        candidate_layers.append(candidates)
    
    # Build baseline matrix from unique candidates
    baseline_matrix = np.zeros((grid_size, grid_size), dtype=int)
    for i in range(len(numbers)):
        if len(valid_configs[i]) == 1:
            _, mat = candidate_layers[i][0]
            baseline_matrix = merge_layers(baseline_matrix, mat)
    
    # Filter candidate layers using baseline compatibility
    filtered_candidate_layers = []
    for i in range(len(candidate_layers)):
        filtered = []
        for (config, mat) in candidate_layers[i]:
            if is_compatible(baseline_matrix, mat):
                filtered.append((config, mat))
        filtered_candidate_layers.append(filtered)
    
    # Backtracking search using filtered candidates
    def search(i, current_matrix, chosen_configs):
        if i == len(numbers):
            return chosen_configs, current_matrix
        for (config, mat) in filtered_candidate_layers[i]:
            if is_compatible(current_matrix, mat):
                new_matrix = merge_layers(current_matrix, mat)
                result = search(i+1, new_matrix, chosen_configs + [config])
                if result is not None:
                    return result
        return None
    
    # Execute search
    solution = search(0, baseline_matrix, [])
    
    if solution is None:
        return None
    
    chosen_configs, final_matrix = solution
    
    # Calculate all trajectory products
    trajectory_products = {}
    for side in ["top", "bottom", "left", "right"]:
        for idx in range(grid_size):
            prod = compute_trajectory_product(final_matrix, side, idx, grid_size)
            trajectory_products[(side, idx)] = prod
    
    return chosen_configs, final_matrix, trajectory_products