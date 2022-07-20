import numpy as np

from shapes.point import Point
from shapes.rectangle import Rectangle, CenteredRectangle
from shapes.shape import Shape



















def solve(SA: Shape, SB: Shape, SC: Shape) -> Shape:
    shapelist = (SA, SB, SC)
    
    # Get inner and outter rectangles
    rs = (s.getInnerRectangle() for s in shapelist)
    Rs = (s.getOutterRectangle() for s in shapelist)
    
    # Analogy on inner and outter rectangles
    rd = Rectangle.analogy(rs[0], rs[1], rs[2])
    Rd = Rectangle.analogy(Rs[0], Rs[1], Rs[2])
    
    r = rd.intersect(Rd)
    
    return 0





#shape = Shape({Point(0,0), Point(10,0), Point(0,5), Point(12,6)})

shape = Shape({ Point(x,y) for x in range(20) for y in range(12) })


R = shape.getOutterRectangle()
r = shape.getInnerRectangle()


options = {'seed': 42, 'n_runs': 100}
shape.getInnerRectangle(method="stochastic", **options)