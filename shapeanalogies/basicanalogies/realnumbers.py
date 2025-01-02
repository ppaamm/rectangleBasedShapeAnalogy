def arithmetic(a:float, b:float, c:float) -> float:
    return c + b - a

def geometric(a:float, b:float, c:float) -> float:
    return c * b / a

def bounded(a:float, b:float, c:float) -> float:
    assert(0 < a and a < 1)
    assert(0 < b and b < 1)
    assert(0 < c and c < 1)
    
    return 1 / (1 + (1-c) * (1-b) * a / ((1-a) * b * c))
    
    
    
    