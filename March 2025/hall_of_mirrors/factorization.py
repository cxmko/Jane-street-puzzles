import itertools

def ultra_factorizations(nums, max_tuple_length, max_factor):
    """
    For each number in the input list 'nums', generate all valid factorizations (as tuples)
    satisfying the following:
      - The product of the factors equals the number.
      - Only factors up to max_factor are allowed.
      - The length of the tuple is at most max_tuple_length.
      - Factor 1, if used, may only appear as the first element, the last element, or both.
    
    Every possible ordering (i.e. permutation) of the factors is produced.
    
    Args:
        nums: List of integers to factorize
        max_tuple_length: Maximum length of factorization tuples
        max_factor: Maximum allowed factor value
        
    Returns:
        A list of lists. The i-th sublist contains all valid factorization tuples for nums[i].
    """
    
    # Memoization dictionary for core factorizations
    memo = {}
    def factorize(n, start, remaining_length):
        """
        Recursively generate all sorted (non-decreasing) tuples of factors (>=2) that multiply to n,
        using factors in the range [start, max_factor]. Only factorizations with total length up
        to the given remaining_length are returned.
        """
        key = (n, start, remaining_length)
        if key in memo:
            return memo[key]
        results = set()
        # Iterate possible factors from 'start' up to min(n, max_factor)
        for f in range(start, min(n, max_factor) + 1):
            if f == 1:
                continue  # core factors never include 1
            if n % f == 0:
                if f == n:
                    # f exactly equals n: valid if we have room for one factor.
                    results.add((f,))
                else:
                    # Only recurse if we can add more factors.
                    if remaining_length > 1:
                        # f must be <= next factors to keep sorted order.
                        for tail in factorize(n // f, f, remaining_length - 1):
                            results.add((f,) + tail)
        memo[key] = results
        return results

    all_results = []
    for n in nums:
        result_set = set()
        # Special handling for n==1.
        if n == 1:
            if max_tuple_length >= 1:
                result_set.add((1,))
            if max_tuple_length >= 2:
                result_set.add((1, 1))
            all_results.append(list(result_set))
            continue

        # Compute core factorizations for n using factors >=2.
        core_set = factorize(n, 2, max_tuple_length)
        # For each core factorization, produce every ordering and add possible boundary 1's.
        for core in core_set:
            # Generate all unique permutations of the core tuple.
            perms = set(itertools.permutations(core))
            for perm in perms:
                # The core permutation itself (without any added 1's)
                if len(perm) <= max_tuple_length:
                    result_set.add(perm)
                # Add a 1 at the beginning, if room.
                if len(perm) + 1 <= max_tuple_length:
                    result_set.add((1,) + perm)
                # Add a 1 at the end, if room.
                if len(perm) + 1 <= max_tuple_length:
                    result_set.add(perm + (1,))
                # Add 1's at both the beginning and end, if room.
                if len(perm) + 2 <= max_tuple_length:
                    result_set.add((1,) + perm + (1,))
        all_results.append(list(result_set))
    return all_results
