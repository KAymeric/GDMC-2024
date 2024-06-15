class Point:
    def __init__(self, x : int = 0, y : int = 0, z : int = 0, p : tuple[int,int,int] = None):
        if p != None: x,y,z = p
        self._x = x
        self._y = y
        self._z = z
        
    @property
    def x(self) -> int:
        return self._x
    @property
    def y(self) -> int:
        return self._y
    @property
    def z(self) -> int:
        return self._z
    @property
    def position(self) -> tuple[int,int,int]:
        return (self._x, self._y, self._z)
    
    @x.setter
    def x(self, value : int):
        self._x = value
    @y.setter
    def y(self, value : int):
        self._y = value
    @z.setter
    def z(self, value : int):
        self._z = value
    @position.setter
    def position(self, value : tuple[int,int,int]):
        self._x, self._y, self._z = value
        
    def __repr__(self):
        return f"Point({self.position})"
    
    def copy(self) -> 'Point':
        return Point(self.x, self.y, self.z)