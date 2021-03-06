# -----------------------------------------------------------------------------
# Graphic interface objects: Xilarius
# Project
# Ana Arellano   		A01089996
# Ana Karen Reyna		A01280310
# -----------------------------------------------------------------------------

from pygame import image, Rect, draw, Surface, font
from pygame.locals import *
from random import randint, choice
from math import sqrt


#Helper to get distance from point to point, given as parameters
def distance(p1, p2):
    return(sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2))


"""
For constant definitions
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
#paths
const.imagespath = "images/"
const.musicpath = "music/"
# Colors
const.white  = (255 , 255 , 255)
const.pink   = (255 , 0 , 255)
const.black  = (0 , 0 , 0)
const.yellow = (255 , 255 , 0)
const.red = (255 , 0 , 0)
const.green = (106, 198, 81)
const.gray = (64,64,64)

const.Pgreen = (192, 234, 68)
const.Porange = (255, 201, 14)
const.Pblue = (18, 204, 214)
#images
const.beginning="door_open"
const.ending ="door_closed"
const.brownPatch = "brown_cell"
const.greenPatch = "green_cell"
const.grayPatch = "stone_block"
const.dirtPatch = "dirt_block"
#directions 
const.right = 0
const.left = 1
const.up = 2
const.down = 3

#Sizes
const.wc = 26 # width of a square on the maze
const.hc = 26 # height of the square on the maze

const.time_character_poll = 75
#Objets
const.instructions =[]
  
    
class Point(object):
    """
    Coordinate or cardinal point
    """
    def __init__(self, xy):
        self.x = xy[0]
        self.y = xy[1]      
    
#Starts cell object
#-------------------------------
class Case(object):
    """
    Case is a square on the maze
    """

    def __init__(self):
        
        self.state = False
        self.gate = [True, True, True, True] # D, G, H, B
        #self.background = CaseImage((0, 0), const.greenPatch)
		
class CaseColor(object):
    """
    For the squares background coloring
    """
    def __init__(self, Pos, color):
        self.pos = Pos
        
        self.surf = Surface((const.wc, const.hc))
        self.surf.fill(color)
class CaseImage(object):
    """
    For the squares background image
    """
    def __init__(self, Pos, imagenam):
        self.pos = Pos
        imagename=const.imagespath+imagenam+".png"
        self.img = image.load(imagename).convert_alpha()
        self.img.set_colorkey(RLEACCEL)
        self.rect_img = self.img.get_rect()
        self.surf = Surface((const.wc, const.hc))
        self.surf.fill(const.green)
        self.surf.blit(self.img,self.rect_img)  
class CaseDoubleImage(object):
    """
    For the squares background image double size
    """
    def __init__(self, Pos, imagenam):
        self.pos = Pos
        imagename=const.imagespath+imagenam+".png"
        self.img = image.load(imagename).convert_alpha()
        self.img.set_colorkey(RLEACCEL)
        self.rect_img = self.img.get_rect()
        self.surf = Surface((const.wc*5, const.hc*2))
        self.surf.fill(const.green)
        self.surf.blit(self.img,self.rect_img)  
class CaseText(object):
    """
    For the squares background image and overlay text
    """
    def __init__(self, Pos,message):
        self.pos = Pos
        self.myfont = font.Font(None, 22)
        self.text = self.myfont.render(message, 1, (10, 10, 10))
        self.rect = self.text.get_rect()
        self.surf = Surface(((const.wc*4)-15, (const.hc*2)-18))
        self.surf.fill(const.white)
        self.rect.centerx = self.surf.get_rect().centerx
        self.surf.blit(self.text,self.rect)  
#Starts character object
#-------------------------------------------
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
        
        self.img_speech=''
        self.speech = ''
        self.maze = maze
        #Set avatar image
        self.img = image.load(const.imagespath+"Character_boy.png").convert_alpha()
        self.img.set_colorkey(RLEACCEL)
        self.rect_img = self.img.get_rect()
        self.rect_img[0], self.rect_img[1] = (self.x * const.wc), (self.y * const.hc)
        ##Sets begin and end
        self.dep = CaseImage((0, 0), const.beginning)
        self.fin = CaseImage(((self.maze.w * const.wc - const.wc), (self.maze.h * const.hc - const.hc)), const.ending)
    #Changes image used as character
    def change_avatar(self,imagenam):
        imagename=const.imagespath+imagenam+".png"
        self.img = image.load(imagename).convert_alpha()
        self.img.set_colorkey(RLEACCEL)
        self.rect_img = self.img.get_rect()
        self.rect_img[0], self.rect_img[1] = (self.x * const.wc), (self.y * const.hc)
   #Display the environment 
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
        self.maze.show(screen)    
        screen.blit(self.dep.surf, self.dep.pos)
        screen.blit(self.fin.surf, self.fin.pos)            
        screen.blit(self.img, self.rect_img)
        if self.img_speech != '':
            screen.blit(self.img_speech.surf, self.img_speech.pos)
            screen.blit(self.speech.surf,self.speech.pos)
        
    #Create bubble of speech    
    def talk(self,message):
        #Checks if the character is on the edges
        #and generates the speech bubble on the oposite direction
        if ((self.x+1)*(const.wc)) >= (self.maze.w *15):
            self.img_speech = CaseDoubleImage((((self.x-5) * const.wc), (self.y * const.hc)),"bubble_small_revert")
            self.speech = CaseText((((self.x-4.4) * const.wc), ((self.y+0.3) * const.hc)),message)
        else:
            self.img_speech = CaseDoubleImage((((self.x+1) * const.wc), (self.y * const.hc)),"bubble_small")
            self.speech = CaseText((((self.x+1.4) * const.wc), ((self.y+0.3) * const.hc)),message)
    #Destroy bubble of speech
    def stop_talk(self):
        self.img_speech = ''
        self.speech = ''
    #Generates the action that involve moving spaces
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
    #Checks if there is a wall in the direction given as parameter
    def isWall(self,dir):
        #Checks if next step has a wall
        if not self.maze.get_cell(self.x, self.y).gate[dir]:
            return False
        else:
            return True
    #Checks if the finish line is on the direction given as paramater
    def isFinishLine(self,x,y):
        if self.maze.get_cell((self.maze.w - 1), (self.maze.h - 1)) != self.maze.get_cell(x,y):
            return False
        else:
            return True
    #Set the goal case(Cell) of the current maze
    def goal(self, dest):
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
            
        
    #Function to evaluate the rest of the path
    #to help get the correct direction to use
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
    #Generates the path to follow according to all the
    #posible directions to go from the current position
    #to the finish line, given as parameters
    def get_goal(self, csource, cdesti):
        
        source = self.maze.get_cell(csource[0], csource[1])
        desti = self.maze.get_cell(cdesti[0], cdesti[1])
        
        actual = desti
        mainroad = []
        const.instructions.append("miPrograma Uno;\n{\ncrearPersonaje Xilarius;")
        while actual and (actual.x != source.x or actual.y != source.y):
            if actual.x == actual.parent.x - 1:
                self.yellow_road.append(actual)
                mainroad.append(const.right)
            if actual.x == actual.parent.x + 1:
                self.yellow_road.append(actual)
                mainroad.append(const.left)
            if actual.y == actual.parent.y - 1:
                self.yellow_road.append(actual)
                mainroad.append(const.down)
            if actual.y == actual.parent.y + 1:
                self.yellow_road.append(actual)
                mainroad.append(const.up)
                
            actual = actual.parent
            
        return_road = []        
        id = len(mainroad) - 1
        
        while id >= 0:
            return_road.append(self.maze.notdir(mainroad[id]))
            id -= 1
            
        const.instructions.append("}")
        return return_road
    #Iluminates solution's path    
    def poll(self):
        if self.mainroad:
            self.move(self.mainroad.pop(0))
            self.yellow_road.pop(0)
            
    def go_to(self, road):
        self.mainroad = road
        
#Starts object maze
#---------------------------------
class maze(object):
    def __init__(self, w = 25, h = 30, sx = 0, sy = 0):
        self.w = w
        self.h = h
        
        self.cases = []
        self.wc = const.wc
        self.hc = const.hc
        
        self.sx = sx
        self.sy = sy
        localY = 0.1
        localX = 0.1
        loop = 1
        for v in range(self.w * self.h):
            a = Case()
            a.x = v % self.w
            a.y = int(v / self.w)
            
            #For coordinate of background
            if v < (self.w * loop):
                localX += 1
            else:
                localX = 0.1
                localY = loop
                loop += 1
            #Random patches generation
            if (localY == 0.1 and localX >= (self.w+0.1) ):
                a.background = CaseColor((localX * self.wc,localY* self.hc),const.green)
            else:
                if randint(0, 50) < 10:
                    a.background = CaseImage((localX* self.wc,localY * self.hc), const.brownPatch)
                elif randint(0,50) < 5:
                    a.background = CaseImage((localX* self.wc,localY * self.hc), const.dirtPatch)
                else:
                    a.background = CaseImage((localX * self.wc,localY* self.hc), const.greenPatch)
                
            self.cases.append(a)
    #Gets cell that is on the coordinates given as parameters
    def get_cell(self, x, y):
        return self.cases[(y*self.w) + x]
    #Filters possible directions to take on the path
    #and the directions of the solution to translate in the actions
    #that are needed
    def notdir(self, dir):
        if dir == const.right:
            const.instructions.append("Xilarius.izquierda(1);")
            return const.left
        if dir == const.left:
            const.instructions.append("Xilarius.derecha(1);")
            return const.right
        if dir == const.up:
            const.instructions.append("Xilarius.abajo(1);")
            return const.down
        if dir == const.down:
            const.instructions.append("Xilarius.arriba(1);")
            return const.up
    #Create new maze
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
    #Renders object Maze            
    def show(self, screen):
        W, H = self.wc, self.hc
        sx , sy = self.sx, self.sy
        #Print background cells
        for cell in self.cases:
            screen.blit(cell.background.surf, cell.background.pos)
        #Generates lines of walls
        for y in range(self.h - 1):
            for x in range(self.w - 1):
                c = self.get_cell(x, y)
                
                if c.gate[const.right]:
                    draw.line(screen, const.gray, (sx + ((x + 1) * W), (sy + (y * H))), (sx + ((x + 1) * W), sy + ((y+1) * H)), 3)
                if c.gate[const.down]:
                    draw.line(screen, const.gray, ((sx + (x * W)), (sy + ((y+1) * H))), (sx + ((x + 1) * W), sy + ((y+1) * H)), 3)
                                     
        x = self.w - 1
        #Creates walls from buttom to top
        for y in range(self.h - 1):
            c = self.get_cell(x, y)
            
            if c.gate[const.down]:
                draw.line(screen, const.gray, ((sx + (x * W)), (sy + ((y+1) * H))), (sx + ((x + 1) * W), sy + ((y+1) * H)), 3)
                
        y = self.h - 1
        #Creates walls from left to right
        for x in range(self.w - 1):
            c = self.get_cell(x, y)
            
            if c.gate[const.right]:
                draw.line(screen, const.gray, (sx + ((x + 1) * W), (sy + (y * H))), (sx + ((x + 1) * W), sy + ((y+1) * H)), 3)
                
        #Draws outline
        draw.rect(screen, const.gray, (sx, sy, W * self.w, H * self.h), 3)
#Instantce of character
class Xilarius(object):
    def __init__(self, Pos):
        self.img = image.load(const.imagespath+"Character_boy.png").convert_alpha()
        self.img.set_colorkey(RLEACCEL)
        self.rect = Rect(Pos, (26, 26))
        
    def show(self, screen):
        screen.blit(self.img, self.rect)