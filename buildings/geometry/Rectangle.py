from gdpc import Editor, Block, geometry
from buildings.geometry.Point import Point

class Rectangle:
    def __init__(self, point1 : Point, point2 : Point):
        self.p1 = point1
        self.p2 = point2
    
    @property    
    def position(self):
        return (self.p1.position, self.p2.position)
    @property
    def height(self):
        return self.p2.y - self.p1.y
    
    def __eq__(self, other) -> bool:
        return self.position == other.position
    
    def copy(self):
        return Rectangle(self.p1.copy(), self.p2.copy())
    
    def fill(self,editor : Editor, material : str, y : int = None, xpadding : int = 0, zpadding : int = 0):
        if self.p2.x - self.p1.x < 2*xpadding: xpadding = 0
        if self.p2.z - self.p1.z < 2*zpadding: zpadding = 0
        if y is None: y = self.p2.y
        
        geometry.placeCuboid(editor, (self.p1.x+xpadding, 0, self.p1.z+zpadding), (self.p2.x-xpadding, y, self.p2.z-zpadding), Block(material))
        
    def is_adjacent(self, other : 'Rectangle') -> bool:
        are_close = lambda a,b : a == b+1 or a == b-1
        is_in_interval = lambda p1,var,p2 : min(p1,p2) <= var <= max(p1,p2)
        switch_axes = lambda axe : 0 if axe == 2 else 2
        
        for point in enumerate(self.position):
            for axe in [0,2]:
                if ((are_close(point[axe], other.position[0][axe]) or 
                     are_close(point[axe], other.position[1][axe])) and
                     is_in_interval(other.position[0][switch_axes(axe)], point[switch_axes(axe)], other.position[1][switch_axes(axe)])):
                    return True
                       
        return False

    def __repr__(self):
        return f"{type(self).__name__}\n1 : {str(self.p1)},\n2 : {str(self.p2)}"