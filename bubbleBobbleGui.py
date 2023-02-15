
from _platform import Platform
from bubbleBobbleGame import BubbleBobbleGame, G1, G2, NESSUNO, ARENA_W
from characters import U_POINTS
import g2d

class BubbleBobbleGui:
    def __init__(self, game: BubbleBobbleGame):
        self._controller = game
        self._image = g2d.load_image("personaggi.png")
        self._maps = g2d.load_image("maps.png")
        self._arena = game.getArena()
    
    def _drawLivesDraghi(self):
        ctr = self._controller
        image = self._image
        # drago verde
        g2d.draw_image_clip(image, (391, 1486, 13, 15), (32 + 5, 32 + 5, 13, 13)) # cuore
        g2d.draw_image_clip(image, (77, 1336, 6, 5), (32 + 5 + 13, 32 + 13, 6, 5)) # il per (x)
        g2d.draw_image_clip(image, (148 + 9*ctr.lives(G1), 1595, 8, 9), (32 + 5 + 13 + 6 + 1, 32 + 5 + 13//2, 8, 9)) # le vite
        # drago blu
        g2d.draw_image_clip(image, (391, 1486, 13, 15), (ARENA_W - 13 - 5 - 32, 32 + 5, 13, 13))
        g2d.draw_image_clip(image, (77, 1373, 6, 5), (ARENA_W - 6 - 32 - 13 - 5, 32 + 5 + 13 - 5, 6, 5))
        g2d.draw_image_clip(image, (148 + 9*ctr.lives(G2), 1595, 8, 9), (ARENA_W - 13 - 32 - 5 - 6 - 2 - 8, 32 + 5 + 13//2, 8, 9))
        
    def _drawPointsWinsDraghi(self):
        ctr = self._controller
        image = self._image
        ptwG1 = ctr.pointsWins(G1)
        ptwG2 = ctr.pointsWins(G2)
        
        g2d.draw_image_clip(image, (573, 1530, 55, 16), (ARENA_W//2 - 55//2, 32 + 5, 55, 16)) # schermo punti generali
        if ptwG1 > 0:
            g2d.draw_image_clip(image, (148 + 9*ptwG1, 1607, 8, 9), (ARENA_W//2 - 16, 32 + 5 + 3, 8, 9))
        if ptwG2 > 0:
            g2d.draw_image_clip(image, (148 + 9*ptwG2, 1619, 8, 9), (ARENA_W//2 + 55//2 - 11, 32 + 5 + 3, 8, 9))
            
    def _drawLevelPointsDraghi(self):
        ctr = self._controller
        image = self._image
        uptG1 = ctr.points(G1) // U_POINTS - 1
        uptG2 = ctr.points(G2) // U_POINTS - 1
        
        if uptG1 >= 0:                         
            g2d.draw_image_clip(image, (165 + uptG1*36, 1315, 16, 9), (ARENA_W//2 - 55//2 + 3, 32 + 5 + 16 + 5, 16, 9)) # del verde
        if uptG2 >= 0:
            g2d.draw_image_clip(image, (165 + uptG2*36, 1352, 16, 9), (ARENA_W//2 + 8, 32 + 5 + 16 + 5, 16, 9)) # del blu
        
    def _drawActors(self):
        actors = self._arena.actors()
        for actor in actors:
            if isinstance(actor, Platform):
                continue
            g2d.draw_image_clip(self._image, actor.symbol(), actor.position())
        
    def tick(self):
        ctr = self._controller
        maps = self._maps
        arena = self._arena
        
        # comandi g1
        if g2d.key_pressed("z"):
            ctr.sparaBolla(G1)
        
        if g2d.key_pressed("ArrowUp"):
            ctr.salta(G1)
            
        if g2d.key_pressed("ArrowRight"):
            ctr.vaiADx(True, G1)
        elif g2d.key_released("ArrowRight"):
            ctr.vaiADx(False, G1)
            
        if g2d.key_pressed("ArrowLeft"):
            ctr.vaiASx(True, G1)
        elif g2d.key_released("ArrowLeft"):
            ctr.vaiASx(False, G1)
        
        # comandi g2
        if g2d.key_pressed("Enter"):
            ctr.sparaBolla(G2)
        
        if g2d.key_pressed("w"):
            ctr.salta(G2)
            
        if g2d.key_pressed("d"):
            ctr.vaiADx(True, G2)
        elif g2d.key_released("d"):
            ctr.vaiADx(False, G2)
            
        if g2d.key_pressed("a"):
            ctr.vaiASx(True, G2)
        elif g2d.key_released("a"):
            ctr.vaiASx(False, G2)
        
        g2d.clear_canvas()
        g2d.draw_image_clip(maps, arena.maps(), arena.position()) # texture
        self._drawLivesDraghi()
        self._drawPointsWinsDraghi()
        self._drawLevelPointsDraghi()
        self._drawActors()
        
        if ctr.gameOver():
            if ctr.win():
                if not ctr.prossimoLivello():
                    winner = ctr.winner()
                    if winner == NESSUNO:
                        winnerStr = "nessuno"
                    else:
                        winnerStr = "drago verde" if winner == G1 else "drago blu"
                    g2d.alert("Fine.\nVincitore: " + winnerStr)
                    g2d.close_canvas()
            else:
                g2d.alert("Game Over.")
                g2d.close_canvas()
            
        ctr.goOnFrame() # prossimo frame
            
def guiPlay(game: BubbleBobbleGame):
    g2d.init_canvas(game.getSize())
    gui = BubbleBobbleGui(game)
    g2d.main_loop(gui.tick)
