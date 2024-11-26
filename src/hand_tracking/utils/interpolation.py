def lerp(start, end, t):
    """Linear interpolation between start and end points"""
    return start + (end - start) * t

def inverse_lerp(start, end, value):
    """Find the corresponding percentage value t of a value in a linear interpolation"""
    return float(((value - start) / (end - start)))

def clamp(_min, _max, _input):
    """clamp a value within min and max values"""
    return min(max(_input, _min), _max)