from actor import Actor
from level import Level
MAPS_AUTHOR = (4608, 3816, 512, 424)

class Arena():
    '''A generic 2D game, with a given size in pixels and a list of actors
    '''
    def __init__(self, size: (int, int)):
        '''Create an arena, with given dimensions in pixels
        '''
        self._w, self._h = size
        self._count = 0
        self._actors = []
        self._levels = []
        self._currentLevel = 0
        self._currentMaps = None

    def _removePlatforms(self):
        platDaRimuovere = self._levels[0].getPlatforms()
        for p in platDaRimuovere:
            self.remove(p)
    
    def _addPlatformsAndEnemies(self):
        platDaAggiungere = self._levels[0].getPlatforms()
        enemDaAggiungere = self._levels[0].getEnemies()
        self._actors += platDaAggiungere + enemDaAggiungere
        
    def nextLevel(self) -> bool:
        if not self._levels:
            return False
        
        self._currentLevel += 1
        if self._currentLevel > 1: # potremmo essere al primo livello...
            self._removePlatforms()
            self._levels.pop(0)
        if self._levels:
            self._addPlatformsAndEnemies()
            self._currentMaps = self._levels[0].getTexture()
        else:
            self._currentMaps = MAPS_AUTHOR
        return True

    def add(self, a: Actor):
        '''Register an actor into this arena.
        Actors are blitted in their order of registration
        '''
        if a not in self._actors:
            self._actors.append(a)
            
    def addLevel(self, l: Level):
        '''Register a level into this arena.
        '''
        if l not in self._levels:
            self._levels.append(l)

    def remove(self, a: Actor):
        '''Cancel an actor from this arena
        '''
        if a in self._actors:
            self._actors.remove(a)

    def moveAll(self):
        '''Move all actors (through their own move method).
        After each single move, collisions are checked and eventually
        the `collide` methods of both colliding actors are called
        '''
        actors = list(reversed(self._actors))
        for a in actors:
            a.move()
            for other in actors:
                # reversed order, so actors drawn on top of others
                # (towards the end of the cycle) are checked first
                if other is not a and self.checkCollision(a, other):
                    a.collide(other)
                    other.collide(a)
        self._count += 1

    def checkCollision(self, a1: Actor, a2: Actor) -> bool:
        '''Check the two actors (args) for mutual collision (bounding-box
        collision detection). Return True if colliding, False otherwise
        '''
        x1, y1, w1, h1 = a1.position()
        x2, y2, w2, h2 = a2.position()
        return (y2 < y1 + h1 and y1 < y2 + h2
            and x2 < x1 + w1 and x1 < x2 + w2
            and a1 in self._actors and a2 in self._actors)
        
    def actors(self) -> list:
        '''Return a copy of the list of actors
        '''
        return list(self._actors)

    def size(self) -> (int, int):
        '''Return the size of the arena as a couple: (width, height)
        '''
        return (self._w, self._h)

    def count(self) -> int:
        '''Return the total count of ticks (or frames)
        '''
        return self._count
    
    def isOutside(self, a: Actor) -> bool:
        x, y, w, h = a.position()
        
        return x >= self._w or x + w <= 0 or y >= self._h or y + h <= 0
    
    def maps(self) -> (int, int, int, int):
        return self._currentMaps
    
    def position(self) -> (int, int, int, int):
        return (0, 0, self._w, self._h)
    