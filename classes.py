"""Classes for use in minesweeper etc."""

from typing import List
from dataclasses import dataclass


@dataclass
class Point:
    """A point on an (x, y) plane."""
    
    x: int
    y: int


class Box:
    """A box in the grid."""
    
    def __init__(self, pos: Point, /, mine: bool = False):
        self.pos = pos
        
        self.is_mine = mine
        self.is_flag = False
        self.num = -1
        self.revealed = False
        
    def get_neighbours(self, box_num: int) -> List[Point]:
        neighbours = []
        
        x_min = max(self.pos.x - 1, 0)
        x_max = min(self.pos.x + 1, box_num - 1)
        y_min = max(self.pos.y - 1, 0)
        y_max = min(self.pos.y + 1, box_num - 1)
        
        for x in range(x_min, x_max + 1):
            for y in range(y_min, y_max + 1):
                if Point(x, y) != self.pos:
                    neighbours.append(Point(x, y))
        
        return neighbours
