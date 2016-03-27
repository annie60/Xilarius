# -----------------------------------------------------------------------------
# Interfaz grafica: Xilarius
# Proyecto
# Ana Arellano   		A01089996
# Ana Karen Reyna		A01280310
# -----------------------------------------------------------------------------

from pygame import image, Rect, draw, Surface
from pygame.locals import *
from random import randint, choice
from math import sqrt


"""
Funcion:
"""

def distance(p1, p2):
    return(sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2))


"""
Para uso de la clase
"""
class def_const(object):
    def __getattr__(self, attr):
        return const.__dict__[attr]
    
    def __setattr__ (self, attr, value):
        if attr in self.__dict__.keys():
            raise Exception("Impossible to declare constant")
        else:
            self.__dict__[attr] = value
            
    def __str__(self):
        return self.__dict__.__str__()


const = def_const ()
"""Contant definitions """

# Colors
const.white  = (255 , 255 , 255)
const.pink   = (255 , 0 , 255)
const.black  = (0 , 0 , 0)
const.yellow = (255 , 255 , 0)
const.red = (255 , 0 , 0)
const.green = (0, 255, 0)

const.Pgreen = (192, 234, 68)
const.Porange = (255, 201, 14)
const.Pblue = (18, 204, 214)

#directions 
const.right = 0
const.left = 1
const.up = 2
const.down = 3

#Sizes

const.wc = 16 # width of a square on the maze
const.hc = 16 # height of the square on the maze

const.time_character_poll = 75

  
    
class Point(object):
    """
    Coordinate or cardinal point
    """
    def __init__(self, xy):
        self.x = xy[0]
        self.y = xy[1]      
    
	
class Case(object):
    """
    Case is a square on the maze
    """

    def __init__(self):
        self.state = False
        self.gate = [True, True, True, True] # D, G, H, B
        
		
class CaseColor(object):
    """
    For the squares coloring
    """
    def __init__(self, Pos, color):
        self.pos = Pos
        
        self.surf = Surface((const.wc, const.hc))
        self.surf.fill(color)
        
		
class Character(object):
    """
    Instance of a character
    """
    def __init__(self, maze):
        self.x = 0
        self.y = 0
        
        self.mainroad = None
        self.yellow_road = []
        self.reverse = 0
        
        self.maze = maze
        #Set avatar image
        self.img = image.load("Bipo.png").convert()
        self.img.set_colorkey(const.pink)
        self.rect_img = self.img.get_rect()
        self.rect_img[0], self.rect_img[1] = (self.x * const.wc), (self.y * const.hc)
        ##Sets begin and end
        self.dep = CaseColor((0, 0), const.green)
        self.fin = CaseColor(((self.maze.w * const.wc - const.wc), (self.maze.h * const.hc - const.hc)), const.red)

        
    def show(self, screen):

        caseL = []
        
        if self.yellow_road:
            
            if self.reverse == 0:
                self.yellow_road.reverse()
                self.reverse = 1
                
            
            for id, c in enumerate(self.yellow_road): 
                    caseL.append(CaseColor(((c.x * const.wc), (c.y * const.hc)), const.yellow))
                    
                    
                
        caseL.reverse()
        for c in caseL:
            screen.blit(c.surf, c.pos)
            
        screen.blit(self.dep.surf, self.dep.pos)
        screen.blit(self.fin.surf, self.fin.pos)            
        screen.blit(self.img, self.rect_img)
        
        
        self.maze.show(screen)
        
    def move(self, dir):
        if not self.maze.get_cell(self.x, self.y).gate[dir]:
            
            if dir == const.right and self.x + 1 < self.maze.w:
                self.x += 1
            if dir == const.left and self.x - 1 >= 0:
                self.x -= 1
            if dir == const.up and self.y - 1 >= 0:
                self.y -= 1
            if dir == const.down and self.y + 1 < self.maze.h:
                self.y += 1
                
            self.rect_img[0], self.rect_img[1] = (self.x * const.wc), (self.y * const.hc)
            
    def astar(self, dest):
        desti = Point(dest)
        openL = []
        closeL = []
        
        debut = self.maze.get_cell(self.x, self.y)
        openL.append(debut)
        
        debut.Fille = distance((self.x, self.y), (desti.x, desti.y))
        debut.Garcon = 0
        debut.Homme = distance((self.x, self.y), (desti.x, desti.y))
        debut.parent = None
        
        while 1:
            if len(openL) <= 0:
                break
            
            min , min_id = openL[0].Fille, 0
            
            for id, cell in enumerate(openL[1:]):
                if cell.Fille < min:
                    min = cell.Fille
                    min_id = id + 1
                    
            closeL.append(openL[min_id])

            
            if openL[min_id].x == desti.x and openL[min_id].y == desti.y:
                break
            
            self._traitement(closeL, openL, openL[min_id].x + 1, openL[min_id].y, const.right, openL[min_id], desti)
            self._traitement(closeL, openL, openL[min_id].x - 1, openL[min_id].y, const.left, openL[min_id], desti)
            self._traitement(closeL, openL, openL[min_id].x, openL[min_id].y - 1, const.up, openL[min_id], desti)
            self._traitement(closeL, openL, openL[min_id].x, openL[min_id].y + 1, const.down, openL[min_id], desti)
            
            openL.remove(openL[min_id])
            
            
        
        
    def _traitement(self, closeL, openL, x, y, dir, parent, desti):
        if parent.gate[dir]:
            return
        
        c = self.maze.get_cell(x, y)
        
        if c in closeL:
            return
        
        if c in openL:
            Garcon = distance((x, y), (parent.x, parent.y))
            c.dir = self.maze.notdir(dir)
            
            if Garcon < c.Garcon:
                c.Garcon = Gracon
                c.Fille = c.Homme + c.Garcon
                c.parent = parent
                
        else:
            c.parent = parent
            c.dir = self.maze.notdir(dir)
            c.Garcon = distance((x, y), (parent.x, parent.y))
            c.Homme = distance((x, y), (desti.x, desti.y))
            c.Fille = c.Homme + c.Garcon
            openL.append(c)
            
    def get_astar(self, csource, cdesti):
        
        source = self.maze.get_cell(csource[0], csource[1])
        desti = self.maze.get_cell(cdesti[0], cdesti[1])
        
        actuel = desti
        mainroad = []
        
        while actuel and (actuel.x != source.x or actuel.y != source.y):
            if actuel.x == actuel.parent.x - 1:
                self.yellow_road.append(actuel)
                mainroad.append(const.right)
            if actuel.x == actuel.parent.x + 1:
                self.yellow_road.append(actuel)
                mainroad.append(const.left)
            if actuel.y == actuel.parent.y - 1:
                self.yellow_road.append(actuel)
                mainroad.append(const.down)
            if actuel.y == actuel.parent.y + 1:
                self.yellow_road.append(actuel)
                mainroad.append(const.up)
                
            actuel = actuel.parent
            
        che_retour = []        
        id = len(mainroad) - 1
        
        while id >= 0:
            che_retour.append(self.maze.notdir(mainroad[id]))
            id -= 1
            
        
        return che_retour
        
    def poll(self):
        if self.mainroad:
            self.move(self.mainroad.pop(0))
            self.yellow_road.pop(0)
            
    def go_to(self, che):
        self.mainroad = che
        
        
class maze(object):
    def __init__(self, w = 25, h = 30, sx = 0, sy = 0):
        self.w = w
        self.h = h
        
        self.cases = []
        self.wc = const.wc
        self.hc = const.hc
        
        self.sx = sx
        self.sy = sy
        
        for v in range(self.w * self.h):
            a = Case()
            a.x = v % self.w
            a.y = int(v / self.w)
            self.cases.append(a)
        
    def get_cell(self, x, y):
        return self.cases[(y*self.w) + x]
    
    def notdir(self, dir):
        if dir == const.right:
            return const.left
        if dir == const.left:
            return const.right
        if dir == const.up:
            return const.down
        if dir == const.down:
            return const.up
        
    def generate_maze(self, x = -1, y = -1):
        if x == -1:
            x = randint(0, self.w - 1)
            y = randint(0, self.h - 1)
            
        cell_act = self.get_cell(x, y)
        
        if not cell_act.state:
            cell_act.state = True
            
            tab = []
            
            if x + 1 < self.w and not self.get_cell(x + 1, y).state:
                tab.append((x + 1, y, const.right))
            if x - 1 >= 0 and not self.get_cell(x - 1, y).state:
                tab.append((x - 1, y, const.left))
            if y + 1 < self.h and not self.get_cell(x, y + 1).state:
                tab.append((x, y + 1, const.down))
            if y - 1 >= 0 and not self.get_cell(x, y - 1).state:
                tab.append((x, y - 1, const.up))
                
                
            if tab:
                while tab:
                    C = choice(tab)
                    
                    if not self.get_cell(C[0], C[1]).state:
                        
                        cell = self.get_cell(C[0], C[1])
                        cell_act.gate[C[2]] = False
                        cell.gate[self.notdir(C[2])] = False
                        self.generate_maze(C[0], C[1])
                    
                    else:
                        tab.remove(C)
                    
    def show(self, screen):
        W, H = self.wc, self.hc
        sx , sy = self.sx, self.sy
        
        for y in range(self.h - 1):
            for x in range(self.w - 1):
                c = self.get_cell(x, y)
                
                if c.gate[const.right]:
                    draw.line(screen, const.black, (sx + ((x + 1) * W), (sy + (y * H))), (sx + ((x + 1) * W), sy + ((y+1) * H)), 2)
                if c.gate[const.down]:
                    draw.line(screen, const.black, ((sx + (x * W)), (sy + ((y+1) * H))), (sx + ((x + 1) * W), sy + ((y+1) * H)), 2)
                                     
        x = self.w - 1
        
        for y in range(self.h - 1):
            c = self.get_cell(x, y)
            
            if c.gate[const.down]:
                draw.line(screen, const.black, ((sx + (x * W)), (sy + ((y+1) * H))), (sx + ((x + 1) * W), sy + ((y+1) * H)), 2)
                
        y = self.h - 1
        
        for x in range(self.w - 1):
            c = self.get_cell(x, y)
            
            if c.gate[const.right]:
                draw.line(screen, const.black, (sx + ((x + 1) * W), (sy + (y * H))), (sx + ((x + 1) * W), sy + ((y+1) * H)), 2)
                
                

        draw.rect(screen, const.black, (sx, sy, W * self.w, H * self.h), 2)

class Xilarius(object):
    def __init__(self, Pos):
        
        self.img = image.load("Bipo.png").convert()
        self.img.set_colorkey(const.pink)
        self.rect = Rect(Pos, (16, 16))
        
    def show(self, screen):
        screen.blit(self.img, self.rect)