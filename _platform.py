from actor import Actor

class Platform(Actor):
    def __init__(self, level, pos: (int, int), w: int, h: int):
        self._x, self._y = pos
        self._w, self._h = w, h
        level.addPlatform(self)
        
    def move(self):
        return

    def collide(self, other: Actor):
        return

    def position(self) -> (int, int, int, int):
        return self._x, self._y, self._w, self._h

    def symbol(self) -> (int, int, int, int):
        return None
    
    def isVerticale(self) -> bool:
        return self._w < self._h