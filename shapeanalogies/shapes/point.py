from dataclasses import dataclass
import numpy as np

@dataclass(eq=True, frozen=True)
class Point:
    x: int
    y: int
    
    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)



def pointDistance(p1: Point, p2: Point) -> int:
    return np.abs(p1.x - p2.x) + np.abs(p1.y - p2.y)