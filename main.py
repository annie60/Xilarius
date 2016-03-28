# -----------------------------------------------------------------------------
# Interfaz grafica: Xilarius
# Proyecto
# Ana Arellano   		A01089996
# Ana Karen Reyna		A01280310
# -----------------------------------------------------------------------------


#-----------------------Libs import-----------------------#
import pygame, sys
from pygame.locals import *
from Function import *
from Class import *
from tygame.main import StaticFrame,Entry, Button, Label, render_widgets, handle_widgets #But you can put in ..\Python\Lib\site-packages
imagespath ="images/"
avatars = ["Character_boy","Character_Cat_girl",
            "Character_Horn_Girl","Character_Pink_Girl"]
avatar_index=0
#TODO Remplazar funciones de botones
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
def Execute_instruction():
    global entryForInput
    #TODO Logica para procesar semantica
    print("Ejecuta")
def Change_avatar():
    global avatar_index,character
    if avatar_index < len(avatars)-1:
        avatar_index+=1
        character.change_avatar(avatars[avatar_index])    
    else:
        avatar_index=0
        character.change_avatar(avatars[avatar_index])
def Character_talk():
    global character,Window
    character.talk(Window,"hello")
# FIN


#---------------------Pygame init--------------------#
pygame.init()


#Window creation
WW, WH = 670, 500
Window = pygame.display.set_mode((WW, WH))
icone = image.load(imagespath+avatars[0]+".png")
icone.set_colorkey(const.pink)
pygame.display.set_icon(icone)
pygame.display.set_caption("Xilarius")
# FIN
Frame = StaticFrame(Window, colour = const.Pblue, header = False, bordercolor = const.Pgreen, borderwidth = 5, width = 229, height = 480)
Frame.place((421, 0))


#---------------------Some variables--------------------#
mymaze = maze(16, 19)
mymaze.generate_maze()
character = Character(mymaze) 
    
character_time = 0

list_x1 = list_xil(WW, WH)
list_x2 = fill_list_x2(list_x1)

pygame.display.flip()
pygame.key.set_repeat(50, 55)

change_button= Button(Window, text = "Cambiar avatar ", width = 95, height = 20, bordercolor = const.Porange, colour = const.yellow, fontsize = 12, target = Change_avatar)
change_button.place((545, 6))

Label_gen = Label(Frame, width = 209, height = 290, htitle = " Instrucciones ", htitlefont = "Verdana", htitlesize = 14, htitlecolor = Color(const.black[0], const.black[1], const.black[2]), colour = Color(const.Pgreen[0], const.Pgreen[1], const.Pgreen[2]))
Label_gen.place((10, 20))

entryForInput = Entry(Frame,width=190,height=270)
entryForInput.place((15,40))
execute_button= Button(Window, text = "Correr mi programa! ", width = 165, height = 60, bordercolor = const.Porange, colour = const.yellow, fontsize = 16, target = Execute_instruction)
execute_button.place((460, 350))

##Main loop starts
while True:
    pygame.time.Clock().tick(10)
    Window.fill(const.Porange)    
    keys = pygame.key.get_pressed()
    for event in handle_widgets():
        if event.type == QUIT:
            quit()
            exit()
    ##TODO: Poner aqui logica para traducir programa
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
        if keys[K_h]:
            But_path()
        if keys[K_t]:#TODO es instantaneo hay que cambiar
            Character_talk()
                
    ##Sets miliseconds between a display loop            
    if pygame.time.get_ticks() - character_time >= const.time_character_poll:
        character_time = pygame.time.get_ticks()
        character.poll()


    character.show(Window)
    render_widgets()
    pygame.display.flip()
    if character.x == character.maze.w - 1 and character.y == character.maze.h - 1:
        pygame.time.delay(300)       
        
        for Xil in list_x2:
            Xil.show(Window)
            pygame.display.flip()                     
            
    
        mymaze = maze(16, 19)
        mymaze.generate_maze()
        character = Character(mymaze)
        
        while True:
            Window.fill(const.Porange)
            character.show(Window)
            render_widgets()
            
            if not list_x2: break
            
            i = 0
            while i < 5:
                list_x2.remove(choice(list_x2))  
                i += 1
           
            
            for Xil in list_x2:
                Xil.show(Window)
            
            pygame.display.flip()
            
        list_x2 = fill_list_x2(list_x1)
