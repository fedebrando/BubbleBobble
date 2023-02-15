
from actor import Actor
from _platform import Platform
W_SPRITES = 1290

class Character(Actor):
    def __init__(self, pos):
        self._x, self._y = pos
        self._w, self._h = 16, 16
        self._speed = 5
        self._dx, self._dy = 0, 0
        self._g = 0.4
        self._last_collision = 0
        self._saltando = False
        self._statiSx = [] # tutti i possibili stati in cui può trovarsi il personaggio
        self._direttoADx = True
    
    def move(self):
        raise NotImplementedError('Abstract method')
            
    def collide(self, other):
        raise NotImplementedError('Abstract method')
    
    def _collideConPiattaforma(self) -> bool:
        actors = self._arena.actors()
        
        for p in actors:
            if isinstance(p, Platform):
                if self._arena.checkCollision(self, p):
                    return True
        return False
                
    def position(self):
        return self._x, self._y, self._w, self._h

    def symbol(self): 
        raise NotImplementedError('Abstract method')
    
    def goLeft(self, go: bool):
        if go:
            self._dx = -self._speed
        elif self._dx < 0:
            self._dx = 0

    def goRight(self, go: bool):
        if go:
            self._dx = self._speed
        elif self._dx > 0:
            self._dx = 0

    def goUp(self, go: bool):
        if self._saltando:
            return
        
        if go:
            self._saltando = True
            self._dy = -self._speedSalto
        else:
            self._saltando = False
            self._dy = 0
            
    def giratoADx(self) -> bool:
        return self._direttoADx
            
    def imgStato(self, stato: str, dx: bool) -> (int, int, int, int):
        for stato_c in self._statiSx:
            if stato in stato_c[0]:
                x, y, w, h = stato_c[1]
                return ((W_SPRITES - x - w) if dx else x, y, w, h)
        return None
            
    def statoAttuale(self) -> (str, bool):
        for stato in self._stati:
            if self._stato == stato[1]:
                return stato[0]
        return None
