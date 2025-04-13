import math

def fit_squares_in_space(num_squares: int, dims: list) -> list:
    """automatically returns idealized layout of squares\n
    num_squares | number of squares to be displayed\n
    dims | dimensions of display area\n
    returns | array containing row and column number for idealized display"""
    dim_ratio = dims[0] / dims[1]
    ideal_ratio = [100, 1]
    for nx in range(1, num_squares):
        ny = math.ceil(num_squares/nx)
        ratio = nx/ny
        if abs(ratio - dim_ratio) < abs(ideal_ratio[0] / ideal_ratio[1] - dim_ratio):
            ideal_ratio = [nx, ny]
    return ideal_ratio

def get_magnitude(in_array: list, hyp=True) -> float:
    """returns magnitude of vector or missing component\n
    in_array | list containing vector\n
    hyp = True | assumes user is finding magnitude. If set to false will use first list element as hypotenuse to find missing componenent\n
    returns | resultant magnitude or vector component"""
    if hyp:
        radical = sum(vec**2 for vec in in_array)
    else:
        radical = in_array[0]**2 - sum(vec**2 for vec in in_array[1:])
    return math.sqrt(radical)

def normalize(in_array: list) -> list:
    """returns the unit vector of a given 2D vector"""
    magnitude = get_magnitude(in_array)
    return [vec / magnitude for vec in in_array] if magnitude else [0, 0]

def common_factors(a: int, b: int) -> list:
    """returns a list of common factors for two integers"""
    return [i for i in range(1, min(a, b) + 1) if a % i == 0 and b % i == 0]

def get_distance(a: tuple, b: tuple) -> float:
    """input two 1D same length arrays [a and b] and return distance between two vector points"""
    if not isinstance(a, list) or not isinstance(b, list):
        raise TypeError("Both inputs must be lists.")
    if len(a) != len(b):
        raise ValueError("Input lists must be of the same length.")
    if any(isinstance(i, list) for i in a) or any(isinstance(j, list) for j in b):
        raise ValueError("Inputs must be 1D lists.")
    
    return (sum((ai - bi)**2 for ai, bi in zip(a, b)))**0.5