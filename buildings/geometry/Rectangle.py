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
    
    def fill(self,editor : Editor, material : str, y : int = None, xpadding : int = 0, zpadding : int = 0):
        if self.p2.x - self.p1.x < 2*xpadding: xpadding = 0
        if self.p2.z - self.p1.z < 2*zpadding: zpadding = 0
        if y is None: y = self.p2.y
        
        geometry.placeCuboid(editor, (self.p1.x+xpadding, 0, self.p1.z+zpadding), (self.p2.x-xpadding, y, self.p2.z-zpadding), Block(material))

    def __repr__(self):
        return f"{type(self).__name__}\n1 : {str(self.p1)},\n2 : {str(self.p2)}"