from dataclasses import dataclass
from typing import Tuple, Set
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



@dataclass
class Rectangle:
    center: Tuple[Point, Point]
    h: int
    w: int
    
    
    def buildFromVertices(topleft: Point, bottomright: Point):
        center = Point(int((topleft.x + bottomright.x)/2), int((topleft.y + bottomright.y)/2))
        h = min(np.abs(center.y - topleft.y), np.abs(center.y - bottomright.y))
        w = min(np.abs(center.x - topleft.x), np.abs(center.x - bottomright.x))
        return Rectangle(center, h, w)
    
    def area(self) -> int:
        return (1 + 2 * self.w) * (1 + 2 * self.h)
    
    def topLeftVertex(self) -> Point:
        return Point(self.center.x - self.w, self.center.y + self.h)
    
    def bottomRightVertex(self) -> Point:
        return Point(self.center.x + self.w, self.center.y - self.h)
    
    def intersect(self, other):
        topleft = Point(max(self.topLeftVertex().x, other.topLeftVertex().x),
                        min(self.topLeftVertex().y, other.topLeftVertex().y))
        
        bottomright = Point(min(self.bottomRightVertex().x, other.bottomRightVertex().x),
                            max(self.bottomRightVertex().y, other.bottomRightVertex().y))
        
        
        return Rectangle.buildFromVertices(topleft, bottomright)
    
    def toShape(self) -> Shape:
        points = {Point(self.center.x - self.w + x, self.center.y - self.h + y) 
                  for x in range(2 * self.w + 1)
                  for y in range(2 * self.h + 1)}
        return Shape(points)
    
    
    
    
class Shape:
    def __init__(self, points: Set[Point]):
        self.points = points
        self.X = [p.x for p in points]
        self.Y = [p.y for p in points]
        self.xmax = max(self.X)
        self.ymax = max(self.Y)
        self.xmin = min(self.X)
        self.ymin = min(self.Y)
        
    def getMaxCoordinates(self) -> Tuple[int, int, int, int]:
        return self.xmin, self.xmax, self.ymin, self.ymax
    
    def getCentroid(self) -> Point:
        x = int(np.mean(self.X))
        y = int(np.mean(self.Y))
        return Point(x,y)
    
    def closestPointInShape(self, point: Point) -> Point:
        return min(self.points, key=lambda p: pointDistance(point, p))
    
    def containsPoint(self, point: Point):
        return point in self.points

    
    def containsPoints(self, points: Set[Point]) -> bool:
        return points.issubset(self.points)
    

    def getOutterRectangle(self) -> Rectangle:
        xmin, xmax, ymin, ymax = self.getMaxCoordinates()
        
        center = Point(int((xmax - xmin) /2), int((ymax - ymin) /2))
        h = ymax - center.y
        w = xmax - center.x
        
        return Rectangle(center, h, w)


    def getInnerRectangle(self) -> Rectangle:
        # Defines the center of the rectangle
        centroid = self.closestPointInShape(self.getCentroid())
        cx = centroid.x
        cy = centroid.y
        
        w = 0
        
        candidates = list()
        
        while(True):
            if not( self.containsPoint(Point(cx-w, 0)) and self.containsPoint(Point(cx + w, 0))):
                # maximal width detected
                break
            
            h = 1
            while(True):
                upper = {Point(x, cy+h) for x in range(cx - w, cx + w + 1)}
                lower = {Point(x, cy-h) for x in range(cx - w, cx + w + 1)}
                if not ( self.containsPoints(upper) and self.containsPoints(lower) ):
                    # The rectangle contains points which are not in the shape
                    break
                h = h+1
            
            candidates.append(Rectangle(centroid, h-1, w))
            w = w+1
            
        
        return max(candidates, key = lambda R: R.area())








def rectangleAnalogy(RA: Rectangle, RB: Rectangle, RC: Rectangle) -> Rectangle:
    center = RC.center + RB.center - RA.center
    h = np.abs(RC.h + RB.h - RA.h)
    w = np.abs(RC.w + RB.w - RA.w)
    return Rectangle(center, h, w)






def solve(SA: Shape, SB: Shape, SC: Shape) -> Shape:
    shapelist = (SA, SB, SC)
    
    # Get inner and outter rectangles
    rs = (s.getInnerRectangle() for s in shapelist)
    Rs = (s.getOutterRectangle() for s in shapelist)
    
    # Analogy on inner and outter rectangles
    rd = rectangleAnalogy(rs[0], rs[1], rs[2])
    Rd = rectangleAnalogy(Rs[0], Rs[1], Rs[2])
    
    r = rd.intersect(Rd)
    
    return 0





#shape = Shape({Point(0,0), Point(10,0), Point(0,5), Point(12,6)})

shape = Shape({ Point(x,y) for x in range(20) for y in range(12) })


R = shape.getOutterRectangle()
r = shape.getInnerRectangle()