from dataclasses import dataclass
import numpy as np
from typing import Tuple
from . point import Point


@dataclass
class CenteredRectangle:
    center: Point
    h: int
    w: int
    
    
    def buildFromVertices(topleft: Point, bottomright: Point):
        center = Point(int((topleft.x + bottomright.x)/2), int((topleft.y + bottomright.y)/2))
        h = min(np.abs(center.y - topleft.y), np.abs(center.y - bottomright.y))
        w = min(np.abs(center.x - topleft.x), np.abs(center.x - bottomright.x))
        return CenteredRectangle(center, h, w)
    
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
        
        
        return CenteredRectangle.buildFromVertices(topleft, bottomright)
    
    
    def toRectangle(self):
        return Rectangle(topLeft = Point(self.center.x - self.w, self.center.y + self.h), 
                         w = 2 * self.w + 1, 
                         h = 2 * self.h + 1)
    
    def analogy(RA, RB, RC):
        center = RC.center + RB.center - RA.center
        h = np.abs(RC.h + RB.h - RA.h)
        w = np.abs(RC.w + RB.w - RA.w)
        return CenteredRectangle(center, h, w)
    
    
    
@dataclass
class Rectangle:
    topLeft: Point
    w: int
    h: int
    
    def area(self) -> int:
        return self.h * self.w
    
    def topLeftVertex(self) -> Point:
        return self.topLeft
    
    def bottomRightVertex(self) -> Point:
        #TODO: Turn this into a property
        return Point(self.topLeft.x + self.w, self.topLeft.y - self.h)
    
    def intersect(self, other):
        topleft = Point(max(self.topLeftVertex().x, other.topLeftVertex().x),
                        min(self.topLeftVertex().y, other.topLeftVertex().y))
        
        bottomright = Point(min(self.bottomRightVertex().x, other.bottomRightVertex().x),
                            max(self.bottomRightVertex().y, other.bottomRightVertex().y))
        
        return Rectangle(topleft, bottomright.x - topleft.x, topleft.y - bottomright.y)
    
    def analogy(RA, RB, RC):
        topLeft = RC.topLeft + RB.topLeft - RA.topLeft
        # TODO: Manage case where RA is flat
        w = int(RC.w * RB.w / RA.w)
        h = int(RC.h * RB.h / RA.h)
        return Rectangle(topLeft, w, h)
    
    
    def extractFrame(self, inner):
        R1 = Rectangle(topLeft = self.topLeft, 
                       w = inner.bottomRightVertex().x - self.topLeft.x,
                       h = self.topLeft.y - inner.topLeft.y)
        R2 = Rectangle(topLeft = Point(inner.topLeft.x + inner.w, self.topLeft.y),
                       w = self.bottomRightVertex().x - inner.bottomRightVertex().x, 
                       h = self.topLeft.y - inner.bottomRightVertex().y)
        R3 = Rectangle(topLeft = Point(inner.topLeft.x, inner.topLeft.y - inner.h),
                       w = self.bottomRightVertex().x - inner.topLeft.x,
                       h = inner.bottomRightVertex().y - self.bottomRightVertex().y)
        R4 = Rectangle(topLeft = Point(self.topLeft.x, inner.topLeft.y), 
                       w = inner.topLeft.x - self.topLeft.x, 
                       h = inner.topLeft.y - self.bottomRightVertex().y)
        return [R1, R2, R3, R4]

    