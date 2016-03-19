# -----------------------------------------------------------------------------
# Interfaz grafica: Xilarius
# Proyecto
# Ana Arellano   		A01089996
# Ana Karen Reyna		A01280310
# -----------------------------------------------------------------------------


#-----------------------Libs import-----------------------#
#from pygame import init, display, Color, key, quit, time, event
import pygame, sys
from pygame.locals import *
from Function import *
from Class import *
#from sys import exit

#Replace this
#---------------------Buttons functions--------------------#
    
def But_X_Y(size):
    
    global mymaze
    global character

    mymaze = maze(size[0], size[1])
    mymaze.generate_maze()
    character = Character(mymaze)
##To find solution
def But_path():

    global character

    character.yellow_road = []
    character.reverse = 0
    character.astar(((character.maze.w - 1), (character.maze.h - 1)))
    chemain = character.get_astar((character.x, character.y), ((character.maze.w - 1), (character.maze.h - 1)))
    character.go_to(chemain)
# FIN


#---------------------Pygame init--------------------#
pygame.init()


#Window creation
WW, WH = 640, 480
Window = pygame.display.set_mode((WW, WH))

#icone = image.load("Bipo.png")
#icone.set_colorkey(const.pink)
#display.set_icon(icone)
pygame.display.set_caption("Xilarius")
# FIN



#---------------------Some variables--------------------#
mymaze = maze(25, 30)
mymaze.generate_maze()
character = Character(mymaze) 
    
character_time = 0

list_x1 = list_xil(WW, WH)
list_x2 = fill_list_x2(list_x1)

pygame.display.flip()
pygame.key.set_repeat(50, 55)



##Main loop starts
while True:
    pygame.time.Clock().tick(10)
    Window.fill(const.Porange)    
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
            pygame.display.update()
    ##Todo: Poner aqui logica para traducir programa
    if keys:
        if keys[K_UP]:
            if not character.yellow_road:
                character.move(const.up)
        if keys[K_DOWN]:
            if not character.yellow_road:
                character.move(const.down)
        if keys[K_LEFT]:
            if not character.yellow_road:
                character.move(const.left)
        if keys[K_RIGHT]:
            if not character.yellow_road:
                character.move(const.right)
                

    if pygame.time.get_ticks() - character_time >= const.time_character_poll:
        character_time = pygame.time.get_ticks()
        character.poll()


    character.show(Window)
    pygame.display.flip()
    
    if character.x == character.maze.w - 1 and character.y == character.maze.h - 1:
        pygame.time.delay(300)       
        
        for Xil in list_x2:
            Xil.show(Window)
            pygame.display.flip()                     
            
    
        mymaze = maze(25, 30)
        mymaze.generate_maze()
        character = character(mymaze)
        
        while True:
            Window.fill(const.Porange)
            character.show(Window)
            render_widgets()
            
            if not list_x2: break
            
            i = 0
            while i < 24:
                list_x2.remove(choice(list_x2))  
                i += 1
           
            
            for Xil in list_x2:
                Xil.show(Window)
            
            display.flip()
            
        list_x2 = Function.fill_list_x2(list_x1)
