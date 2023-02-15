
from _platform import Platform
from characters import Enemy

class Level:
    def __init__(self, arena, n: int, texture: (int, int, int, int)):
        self._n = n
        self._texture = texture
        self._platforms = []
        self._enemies = []
        self._arena = arena
        arena.addLevel(self)
    
    def addPlatform(self, p: Platform):
        self._platforms.append(p)
        
    def addEnemy(self, e: Enemy):
        self._enemies.append(e)
        e.setArena(self._arena)
        
    def getN(self) -> int:
        return self._n
    
    def getTexture(self) -> (int, int, int, int):
        return self._texture
    
    def getPlatforms(self) -> [Platform]:
        return self._platforms
    
    def getEnemies(self) -> [Enemy]:
        return self._enemies
    