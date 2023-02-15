
from _platform import Platform
from arena import Arena
from characters import *
from random import randint
from level import Level
ARENA_W, ARENA_H = 509, 424
G1, G2, NESSUNO = 1, 2, 0

class BubbleBobbleGame:
    def __init__(self):
        self._arena = Arena((ARENA_W, ARENA_H))
        arena = self._arena
        
        # lettura personaggi
        with open("config.cfg", "r") as config:
            try:
                for line in config:
                    line = line.split(' ')
                    
                    if line[0] == "dragon1":
                        self._dragon1 = Dragon(arena, (int(line[1]), int(line[2])), True)
                    elif line[0] == "dragon2":
                        self._dragon2 = Dragon(arena, (int(line[1]), int(line[2])), False)
                    elif line[0] == "level":
                        l = Level(arena, int(line[1]), (int(line[2]), int(line[3]), int(line[4]), int(line[5])))
                    elif line[0] == "enemy":
                        Enemy(l, (int(line[1]), int(line[2])))
                    elif line[0] == "platform":
                        Platform(l, (int(line[1]), int(line[2])), int(line[3]), int(line[4]))
            except OSError as e:
                print(e)
            except ValueError as e:
                print(e)
            except:
                print("Errore non specificato.")
                
        self._arena.nextLevel()
    
    def _aggiornaPointsWins(self):
        ptG1 = self._dragon1.points()
        ptG2 = self._dragon2.points()
        
        if ptG1 > ptG2:
            self._dragon1.incPointsWins()
        elif ptG2 > ptG1:
            self._dragon2.incPointsWins()
            
        self._dragon1.resetPoints()
        self._dragon2.resetPoints()
        
    def _resetPositionDraghi(self):
        self._dragon1.resetPosition()
        self._dragon2.resetPosition()
        
    def prossimoLivello(self) -> bool:
        self._aggiornaPointsWins()
        self._resetPositionDraghi()
        
        return self._arena.nextLevel()
    
    def getArena(self):
        return self._arena
    
    def getSize(self) -> (int, int):
        return self._arena.size()
    
    def getActors(self):
        return self._arena.actors()
    
    def goOnFrame(self):
        self._arena.moveAll()
    
    def sparaBolla(self, player: int):
        if player == G1:
            self._dragon1.shootBubble()
        elif player == G2:
            self._dragon2.shootBubble()
        
    def salta(self, player: int):
        if player == G1:
            self._dragon1.goUp(True)
        elif player == G2:
            self._dragon2.goUp(True)
    
    def vaiADx(self, go: bool, player: int):
        if player == G1:
            self._dragon1.goRight(go)
        elif player == G2:
            self._dragon2.goRight(go)
        
    def vaiASx(self, go: bool, player: int):
        if player == G1:
            self._dragon1.goLeft(go)
        elif player == G2:
            self._dragon2.goLeft(go)
            
    def lives(self, player: int) -> int:
        if player == G1:
            return self._dragon1.lives()
        elif player == G2:
            return self._dragon2.lives()
        return None
        
    def points(self, player: int) -> int:
        if player == G1:
            return self._dragon1.points()
        elif player == G2:
            return self._dragon2.points()
        return None
    
    def pointsWins(self, player: int) -> int:
        if player == G1:
            return self._dragon1.pointsWins()
        elif player == G2:
            return self._dragon2.pointsWins()
        return None
            
    def gameOver(self) -> bool:
        return self._dragon1.isMorto() and self._dragon2.isMorto() or self.win()
        
    def win(self) -> bool:
        actors = self._arena.actors()
        
        for a in actors:
            if isinstance(a, Enemy) or isinstance(a, Bubble):
                return False
        return True
    
    def winner(self) -> int:
        totG1 = self._dragon1.pointsWins()
        totG2 = self._dragon2.pointsWins()
        
        if totG1 != totG2:
            return G1 if totG1 > totG2 else G2
        else:
            return NESSUNO
        
    