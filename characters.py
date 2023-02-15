
from character import Character
from actor import Actor
from _platform import Platform
from random import randint, choice
U_POINTS = 100 # punti all'uccisione di un nemico

class Dragon(Character):
    def __init__(self, arena, pos, isGreen: bool):
        super().__init__(pos)
        self._xStart = self._x
        self._yStart = self._y
        self._speedSalto = 10
        self._lives = 9
        self._pt = 0
        self._ptWins = 0
        self._isGreen = isGreen
        
        # immunità dopo un urto con un nemico
        self._immune = False
        self._frmImmune = 60
        self._frmImmuneAttuali = self._frmImmune
        self._frmLampo = 5
        
        # un passo del draghetto
        self._frmPasso = 5
        self._frmPassoAttuali = self._frmPasso
        self._nPasso = 0
        
        # apertura della bocca
        self._sparando = False
        self._frmRicaricaBolla = 5
        self._frmRicaricaAttuali = self._frmRicaricaBolla
        
        w = self._w
        h = self._h
        if isGreen:
            self._statiSx = [("fermo", (6, 16, w, h)), ("spara", (27, 36, w, h)), ("passo0", (27, 16, w, h)), ("passo1", (48, 16, w, h)), ("passo2", (70, 16, w, h)), ("salta", (217, 36, w, h)), ("cade", (195, 36, w, h))]
            self._stato = (6, 16, w, h)
        else:
            self._statiSx = [("fermo", (329, 16, w, h)), ("spara", (350, 36, w, h)), ("passo0", (350, 16, w, h)), ("passo1", (371, 16, w, h)), ("passo2", (393, 16, w, h)), ("salta", (540, 36, w, h)), ("cade", (518, 36, w, h))]
            self._stato = (329, 16, w, h)
            
        self._arena = arena
        arena.add(self)
            
    def move(self):
        arena_w, arena_h = self._arena.size()
        
        self._setStato()
        
        if self._immune:
            self._frmImmuneAttuali -= 1
            if self._frmImmuneAttuali == 0:
                self._immune = False
                self._frmImmuneAttuali = self._frmImmune
        
        if self._saltando or not self._collideConPiattaforma():
            self._saltando = True
            self._dy += self._g
            
        self._y += self._dy
        if self._y > arena_h - self._h:
            self._y = arena_h - self._h

        self._x += self._dx
        if self._x < 0:
            self._x = 0
        elif self._x > arena_w - self._w:
            self._x = arena_w - self._w
        
        if self._dx > 0:
            self._direttoADx = True
        elif self._dx < 0:
            self._direttoADx = False
        
        self._frmPassoAttuali -= 1
        if self._frmPassoAttuali == 0:
            self._nPasso = (self._nPasso + 1) % 3
            self._frmPassoAttuali = self._frmPasso
            
        if self._sparando:
            self._frmRicaricaAttuali -= 1
            if self._frmRicaricaAttuali == 0:
                self._frmRicaricaAttuali = self._frmRicaricaBolla
                self._sparando = False
                
        if self.isMorto():
            if self._lives != 0:
                self._lives = 0
            if self._pt != 0:
                self._pt = 0
            self._arena.remove(self)
    
    def incPoints(self):
        if self._pt < 10*U_POINTS: # cioè di 901 (si va di 100 in 100, ma non oltre 1000)
            self._pt += U_POINTS
    
    def resetPoints(self):
        self._pt = 0
            
    def incPointsWins(self):
        self._ptWins += 1
        
    def resetPosition(self):
        self._x, self._y = self._xStart, self._yStart
        self._direttoADx = True
    
    def shootBubble(self):
        if not self._immune:
            self._sparando = True
            dx = self.giratoADx()
            Bubble(self._arena, (self._x, self._y), dx, self._isGreen)

    def lives(self) -> int:
        return self._lives
    
    def points(self) -> int:
        return self._pt
    
    def pointsWins(self) -> int:
        return self._ptWins

    def collide(self, other):
        if isinstance(other, Platform):
            xp, yp, wp, hp = other.position()
            aDx = self.giratoADx()
            add = (self._w if aDx else 0)
            
            if self._dy > 0 and self._y + self._h - self._dy - self._g <= yp: # drago in caduta
                self._y = yp - self._h
                self._saltando = False
                self.goUp(False)
            elif self._dy < 0 and other.isVerticale() and xp <= self._x + add and self._x + add <= xp + wp: # in salto
                if self._y + self._w > yp + hp:
                    self._dy *= -1
                else:
                    self._dx = 0
                    self._x = xp + (-self._w if aDx else wp)
            elif self._dx > 0 and self._x + self._w < xp + self._w: # diretto a dx
                self._x = xp - self._w
            elif self._dx < 0 and self._x + self._w > xp + wp: # diretto a sx
                self._x = xp + wp
        elif isinstance(other, Enemy):
            if not self._immune:
                self._lives -= 1
                self._immune = True

    def _setStato(self):
        dx = self._dx
        dy = self._dy
        imgStato = self.imgStato
        nPasso = self._nPasso
        
        if self._sparando:
            if self.giratoADx():
                self._stato = imgStato("spara", True)
            else:
                self._stato = imgStato("spara", False)
            return
        if dx > 0 and dy == 0:
            self._stato = imgStato("passo" + str(nPasso), True)
        elif dx < 0 and dy == 0:
            self._stato = imgStato("passo" + str(nPasso), False)
        elif dx > 0 and dy < 0:
            self._stato = imgStato("salta", True)
        elif dx < 0 and dy < 0:
            self._stato = imgStato("salta", False)
        elif dx == 0 and dy < 0:
            if self.giratoADx():
                self._stato = imgStato("salta", True)
            else:
                self._stato = imgStato("salta", False)
        elif dx > 0 and dy > 0:
            self._stato = imgStato("cade", True)
        elif dx < 0 and dy > 0:
            self._stato = imgStato("cade", False)
        elif dx == 0 and dy > 0:
            if self.giratoADx():
                self._stato = imgStato("cade", True)
            else:
                self._stato = imgStato("cade", False)
        elif dx == 0 and dy == 0:
            if self.giratoADx():
                self._stato = imgStato("fermo", True)
            else:
                self._stato = imgStato("fermo", False)
            
    def symbol(self):
        if self._immune and ((self._frmImmune - self._frmImmuneAttuali) % (2*self._frmLampo + 1)) <= 5:
            return 625, 240, self._w, self._h  # sottoimmagine vuota (per il lampeggio)
        return self._stato
    
    def isImmune(self):
        return self._immune

    def isMorto(self) -> bool:
        return self._y + self._h >= self._arena.size()[1] or self._lives == 0
    

class Bubble(Actor):
    def __init__(self, arena: 'Arena', pos: (int, int), direttaADx: bool, isGreen: bool):
        self._x, self._y = pos
        self._xi = self._x
        self._w, self._h = 14, 14
        self._arena = arena
        self._dx, self._dy = 3 if direttaADx else -3, 0
        
        # per il percorso solo orizzontale della bolla
        self._frmOrizz = 20
        self._frmAttuali = self._frmOrizz
        
        self._hasEnemy = False
        self._scoppiata = False
        self._frmScoppiata = 30
        
        w, h = self._w, self._h
        if isGreen:
            self._stati = [("punti", (166, 1315, w, h)), ("conNemico", (322, 245, w, h + 2)), ("mini", (7, 1050, w, h)), ("media", (24, 1050, w, h)), ("grande", (42, 1050, w, h)), ("grandeTonda", (25, 1073, w, h)), ("grandeOvale", (7, 1072, w, h + 2)), ("grandePiuOvale", (44, 1072, w, h + 2))]
        else:
            self._stati = [("punti", (166, 1352, w, h)), ("conNemico", (376, 245, w, h + 2)), ("mini", (330, 1050, w, h)), ("media", (347, 1050, w, h)), ("grande", (365, 1050, w, h)), ("grandeTonda", (79, 1073, w, h)), ("grandeOvale", (61, 1072, w, h + 2)), ("grandePiuOvale", (98, 1072, w, h + 2))]
        self._stato = (7, 1050, w, h)
        arena.add(self)
    
    def changeHasEnemy(self):
        self._hasEnemy = not self._hasEnemy
    
    def move(self):
        self._setSymbolValues()
        
        if self._scoppiata:
            if self._frmScoppiata == 0:
                self._arena.remove(self)
            self._frmScoppiata -= 1
            
        if self._frmAttuali <= self._frmOrizz//3 and self._dx != 0:
            self._dx, self._dy = self._dx + (1 if self._dx < 0 else -1)*0.05, self._dy - 0.05
        
        self._x += self._dx
        self._y += self._dy
        
        if self._arena.isOutside(self):
            self._arena.remove(self)
            
        self._frmAttuali -= 1
        
    def collide(self, other: 'Actor'):
        if isinstance(other, Dragon):
            if self.hasEnemy() and not other.isImmune() and not self._scoppiata:
                self._scoppiata = True
                other.incPoints()
    
    def hasEnemy(self):
        return self._hasEnemy

    def position(self) -> (int, int, int, int):
        return self._x, self._y, self._w, self._h
    
    def _imgStato(self, stato: str) -> (int, int, int, int):
        for stato_c in self._stati:
            if stato in stato_c[0]:
                return stato_c[1]
        return None
          
    def _setSymbolValues(self):
        if self._scoppiata: # visualizza punteggio
            self._stato = self._imgStato("punti")
          
        elif self._hasEnemy: # bolla con nemico
            self._stato = self._imgStato("conNemico")
        else:
            if (d := abs(self._x - self._xi)) <= 4*abs(self._dx): # bolla appena creata
                dx = abs(self._dx)
                if d == 0:
                    self._stato = self._imgStato("mini")
                elif d == 4*dx:
                    self._stato = self._imgStato("media")
                elif d == 8*dx:
                    self._stato = self._imgStato("grande")
                return
                
            if self._dx > 0 and self._dy == 0 or self._dx < 0 and self._dy == 0: # bolla tonda
                self._stato = self._imgStato("grandeTonda")
            elif self._dx > 0 and self._dy < -2 or self._dx < 0 and self._dy < -2: # bolla ancora più ovale
                self._stato = self._imgStato("grandePiuOvale")
            elif self._dx > 0 and self._dy < -1 or self._dx < 0 and self._dy < -1: # bolla ovale
                self._stato = self._imgStato("grandeOvale")

    def symbol(self) -> (int, int, int, int):            
        return self._stato
        
        
class Enemy(Character):
    def __init__(self, level, pos: (int, int)):
        super().__init__(pos)
        self._speed = 2
        self._speedSalto = 9
        self._frmCambioStato = 0
        self._arena = None
        
        # per il passo del nemico
        self._frmPasso = 5
        self._frmPassoAttuali = self._frmPasso
        self._nPasso = 0
        
        w = self._w
        h = self._h
        self._statiSx = [("passo0", (6, 246, w, h)), ("passo1salta", (25, 245, w, h + 1)), ("passo2", (43, 246, w, h)), ("passo3cade", (62, 245, w, h + 1))]
        self._stato = (6, 246, w, h)
        
        level.addEnemy(self)
    
    def setArena(self, arena):
        self._arena = arena

    def _cambioStato(self):
        goLeft = choice([True, False])
    
        self.goUp(choice([True, False]))
        self.goLeft(goLeft)
        self.goRight(not goLeft)
        self._frmCambioStato = randint(60, 150)
        if self._dx > 0:
            self._direttoADx = True
        elif self._dx < 0:
            self._direttoADx = False
        
    def _cambiaDirezione(self):
        self._dx *= -1
    
    def move(self):
        self._setStato()
        if self._frmCambioStato == 0:
            self._cambioStato()
            
        arena_w, arena_h = self._arena.size()
        
        if self._saltando or not self._collideConPiattaforma():
            self._saltando = True
            self._dy += self._g
            
        self._y += self._dy
        if self._y > arena_h - self._h:
            self._y = arena_h - self._h

        self._x += self._dx
        if self._x < 0:
            self._x = 0
        elif self._x > arena_w - self._w:
            self._x = arena_w - self._w
            
        if self._y == arena_h - self._h:
            #self.muori()
            self._y = 0
        elif self._x == 0 or self._x == arena_w - self._w:
            self._cambiaDirezione()
        
        self._frmPassoAttuali -= 1
        if self._frmPassoAttuali == 0:
            self._nPasso = (self._nPasso + 1) % 4
            self._frmPassoAttuali = self._frmPasso
            
        self._frmCambioStato -= 1
            
    def collide(self, other):
        if isinstance(other, Platform):
            xp, yp, wp, hp = other.position()
            aDx = self.giratoADx()
            add = (self._w if aDx else 0)
            
            if self._dy > 0 and self._y + self._h - self._dy - self._g <= yp:
                self._y = yp - self._h
                self._saltando = False
                self.goUp(False)
            elif self._dy < 0 and other.isVerticale() and xp <= self._x + add and self._x + add <= xp + wp:
                if self._y + self._w > yp + hp:
                    self._dy *= -1
                else:
                    self._dx = 0
                    self._x = xp + (-self._w if aDx else wp)
            elif self._dx > 0 and self._x + self._w < xp + self._w:
                self._x = xp - self._w
                self._cambiaDirezione()
            elif self._dx < 0 and self._x + self._w > xp + wp:
                self._x = xp + wp
                self._cambiaDirezione()
        elif isinstance(other, Bubble): # morte
            if not other.hasEnemy():
                other.changeHasEnemy()
                self.muori()

    def _setStato(self):
        dx = self._dx
        dy = self._dy
        imgStato = self.imgStato
        nPasso = self._nPasso
        
        if dx > 0 and dy == 0:
            self._stato = imgStato("passo" + str(nPasso), True)
        elif dx < 0 and dy == 0:
            self._stato = imgStato("passo" + str(nPasso), False)
        elif dx > 0 and dy < 0:
            self._stato = imgStato("salta", True)
        elif dx < 0 and dy < 0:
            self._stato = imgStato("salta", False)
        elif dx == 0 and dy < 0:
            if self.giratoADx():
                self._stato = imgStato("salta", True)
            else:
                self._stato = imgStato("salta", False)
        elif dx > 0 and dy > 0:
            self._stato = imgStato("cade", True)
        elif dx < 0 and dy > 0:
            self._stato = imgStato("cade", False)
        elif dx == 0 and dy > 0:
            if self.giratoADx():
                self._stato = imgStato("cade", True)
            else:
                self._stato = imgStato("cade", False)
        elif dx == 0 and dy == 0:
            if self.giratoADx():
                self._stato = imgStato("passo" + str(nPasso), True)
            else:
                self._stato = imgStato("passo" + str(nPasso), False)        

    def symbol(self):   
        return self._stato
    
    def muori(self):
        self._arena.remove(self)