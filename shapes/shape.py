from typing import Tuple, Set
import numpy as np
from . point import Point, pointDistance
from . rectangle import CenteredRectangle, Rectangle



class Shape:
    def __init__(self, points: Set[Point]):
        self.points = points
        self.X = [p.x for p in points]
        self.Y = [p.y for p in points]
        self.xmax = max(self.X)
        self.ymax = max(self.Y)
        self.xmin = min(self.X)
        self.ymin = min(self.Y)
        
        
    def fromCenteredRectangle(rectangle: CenteredRectangle):
        points = {Point(rectangle.center.x - rectangle.w + x, 
                        rectangle.center.y - rectangle.h + y) 
                  for x in range(2 * rectangle.w + 1)
                  for y in range(2 * rectangle.h + 1)}
        return Shape(points)
    
    
    def fromRectangle(rectangle: Rectangle):
        points = {Point(rectangle.topLeft.x + x, 
                        rectangle.topLeft.y - y)
                  for x in range(rectangle.w)
                  for y in range(rectangle.h)}
        return Shape(points)
    
    
        
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
    

    def getOutterCenteredRectangle(self) -> CenteredRectangle:
        xmin, xmax, ymin, ymax = self.getMaxCoordinates()
        
        center = Point(int((xmax - xmin) /2), int((ymax - ymin) /2))
        h = ymax - center.y
        w = xmax - center.x
        
        return CenteredRectangle(center=center, h=h, w=w)
    
    
    def getOutterRectangle(self) -> Rectangle:
        xmin, xmax, ymin, ymax = self.getMaxCoordinates()
        
        topleft = Point(xmin, ymax)
        h = ymax - ymin
        w = xmax - xmin
        return Rectangle(topLeft=topleft, w=w, h=h)
    


    def getInnerCenteredRectangle(self) -> CenteredRectangle:
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
            
            candidates.append(CenteredRectangle(centroid, h-1, w))
            w = w+1
            
        
        return max(candidates, key = lambda R: R.area())
    
    
    
    def getInnerRectangleStochastic(self, **kwargs) -> Rectangle:
        seed = kwargs.get('seed', 42)
        n_runs = kwargs.get('n_runs', 100)
        
        np.random.seed(seed)
        
        candidates = list()
        
        for i in range(n_runs):
            topLeft = np.random.choice(list(self.points))
            candidates.append(self.extendInnerRectangleFromTopLeft(topLeft))
        
        return max(candidates, key = lambda R: R.area())
    
    
    ############################################################################
    # TODO: Better algorithm to find the best inner rectangle
    
    def maxWidthAtRightOfPoint(self, point: Point) -> int:
        max_w = 0
        while(True):
            if not(self.containsPoint(Point(point.x + max_w + 1, point.y))): return max_w
            max_w = max_w + 1
            
    def maxHeightUnderPoint(self, point: Point) -> int:
        max_h = 0
        while(True):
            if not(self.containsPoint(Point(point.x, point.y - max_h - 1))): return max_h
            max_h = max_h + 1
            
    
    def extendInnerRectangleFromTopLeft(self, topLeft: Point) -> Rectangle:
        candidates = list()
        
        max_h = self.maxHeightUnderPoint(topLeft)
        max_w = self.maxWidthAtRightOfPoint(topLeft)
        
        for w in range(max_w + 1):
            h = self.maxHeightUnderPoint(Point(topLeft.x + w, topLeft.y))
            if h < max_h: max_h = h
            candidates.append(Rectangle(topLeft, w, max_h))
        return max(candidates, key = lambda R: R.area())
    
    
    def getInnerRectangle(self, method="center", **kwargs) -> Rectangle:
        if method == "stochastic":    
            return self.getInnerRectangleStochastic(**kwargs)
        
        # If none of the above
        return self.getInnerCenteredRectangle().toRectagle()
    
    
    