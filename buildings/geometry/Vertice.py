from utils.Enums import DIRECTION
from buildings.geometry.Point import Point
from buildings.geometry.Rectangle import Rectangle

class Vertice(Rectangle):
    def __init__(self, point1 : Point, point2 : Point, facing : DIRECTION = None):
        Rectangle.__init__(self, point1, point2)
        self.facing = facing
    
    @property    
    def neighbors(self) -> list[Point]:
        match self.facing:
            case DIRECTION.NORTH | DIRECTION.SOUTH:
                return [Point(x = self.p1.x - 1, z = self.p1.z), 
                        Point(x = self.p2.x + 1, z = self.p2.z)]
            case DIRECTION.EAST | DIRECTION.WEST:
                return [Point(x = self.p1.x, z = self.p1.z - 1), 
                        Point(x = self.p2.x, z = self.p2.z + 1)]

    def __len__(self):
        return self.p2.x - self.p1.x + self.p2.z - self.p1.z + 1
    
    def __repr__(self):
        return super().__repr__() + f"\nFacing : {self.facing} \n\n"
        