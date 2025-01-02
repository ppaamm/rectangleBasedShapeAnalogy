from dataclasses import dataclass
import numpy as np
from typing import Tuple
from . point import Point
from ..basicanalogies import realnumbers as real_analogies


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
    
    
    def containsRectangle(self, R) -> bool:
        bottomCondition = (self.center.y - self.h <= R.center.y - R.h)
        topCondition = (self.center.y + self.h >= R.center.y + R.h)
        leftCondition = (self.center.x - self.w <= R.center.x - R.w)
        rightCondition = (self.center.x + self.w >= R.center.x + R.w)
        return bottomCondition and topCondition and leftCondition and rightCondition
    
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
    
    
    def containsRectangle(self, R) -> bool:
        bottomCondition = (self.bottomRightVertex().y <= R.bottomRightVertex().y )
        topCondition = (self.topLeftVertex().y >= R.topLeftVertex().y)
        leftCondition = (self.topLeftVertex().x <= R.topLeftVertex().x)
        rightCondition = (self.bottomRightVertex().x >= R.bottomRightVertex().x)
        return bottomCondition and topCondition and leftCondition and rightCondition
    
    
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



class BiRectangle:
    def __init__(self, outerRectangle: Rectangle, innerRectangle: Rectangle):
        assert outerRectangle.containsRectangle(innerRectangle), "Inner rectangle should be contained by outter rectangle"
        
        self.innerRectangle = innerRectangle
        self.outerRectangle = outerRectangle
    
    
    def __repr__(self):
        return "Outer: " + str(self.outerRectangle) + "\nInner: " + str(self.innerRectangle)
    
    def __str__(self):
        return "Outer: " + str(self.outerRectangle) + "\nInner: " + str(self.innerRectangle)
    
    def analogy(BRA, BRB, BRC):
        outerD = Rectangle.analogy(BRA.outerRectangle, BRB.outerRectangle, BRC.outerRectangle)
        
        # Geometrical analogy on the rescaled inner rectangles
        xA_rescale = (BRA.innerRectangle.topLeft.x - BRA.outerRectangle.topLeft.x) / BRA.outerRectangle.w
        xB_rescale = (BRB.innerRectangle.topLeft.x - BRB.outerRectangle.topLeft.x) / BRB.outerRectangle.w
        xC_rescale = (BRC.innerRectangle.topLeft.x - BRC.outerRectangle.topLeft.x) / BRC.outerRectangle.w
        xD_rescale = real_analogies.bounded(xA_rescale, xB_rescale, xC_rescale)
        xD = outerD.topLeft.x + outerD.w * xD_rescale
        
        yA_rescale = (- BRA.innerRectangle.topLeft.y + BRA.outerRectangle.topLeft.y) / BRA.outerRectangle.h
        yB_rescale = (- BRB.innerRectangle.topLeft.y + BRB.outerRectangle.topLeft.y) / BRB.outerRectangle.h
        yC_rescale = (- BRC.innerRectangle.topLeft.y + BRC.outerRectangle.topLeft.y) / BRC.outerRectangle.h
        yD_rescale = real_analogies.bounded(yA_rescale, yB_rescale, yC_rescale)
        yD = outerD.topLeft.y - outerD.h * yD_rescale
        
        
        
        wA_rescale = (BRA.innerRectangle.w + BRA.innerRectangle.topLeft.x 
                      - BRA.outerRectangle.topLeft.x) / BRA.outerRectangle.w
        wB_rescale = (BRB.innerRectangle.w + BRB.innerRectangle.topLeft.x 
                      - BRB.outerRectangle.topLeft.x) / BRB.outerRectangle.w
        wC_rescale = (BRC.innerRectangle.w + BRC.innerRectangle.topLeft.x 
                      - BRC.outerRectangle.topLeft.x) / BRC.outerRectangle.w 
        wD_rescale = real_analogies.bounded(wA_rescale, wB_rescale, wC_rescale)
        wD = outerD.topLeft.x - xD + outerD.w * wD_rescale
        
        
        hA_rescale = (BRA.innerRectangle.h - BRA.innerRectangle.topLeft.y 
                      + BRA.outerRectangle.topLeft.y) / BRA.outerRectangle.h
        hB_rescale = (BRB.innerRectangle.h - BRB.innerRectangle.topLeft.y 
                      + BRB.outerRectangle.topLeft.y) / BRB.outerRectangle.h
        hC_rescale = (BRC.innerRectangle.h - BRC.innerRectangle.topLeft.y 
                      + BRC.outerRectangle.topLeft.y) / BRC.outerRectangle.h 
        hD_rescale = real_analogies.bounded(hA_rescale, hB_rescale, hC_rescale)
        hD = yD - outerD.topLeft.y + outerD.h * hD_rescale
        
        
        innerD = Rectangle(Point(int(xD), int(yD)), int(wD), int(hD))
        
        return BiRectangle(outerD, innerD)
        


