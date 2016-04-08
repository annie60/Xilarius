# -----------------------------------------------------------------------------
# Interfaz grafica: Xilarius
# Proyecto
# Ana Arellano   		A01089996
# Ana Karen Reyna		A01280310
# -----------------------------------------------------------------------------


#-----------------------Libs import-----------------------#
from __future__ import print_function
import pygame, sys, ast
from pygame.locals import *
from Function import *
from Class import *
from tygame.main import StaticFrame,Entry, Button, Label, render_widgets, handle_widgets #But you can put in ..\Python\Lib\site-packages
avatars = ["Character_boy","Character_Cat_girl",
            "Character_Horn_Girl","Character_Pink_Girl"]
avatar_index=0
main_background = "Main_Background"
on_game = False
on_initial = True
blinker_on=True
#------------Virtual Machine---------------#

#Mapeo de memoria
#1000 - 19999 <- Globales
#20000- 24999 <- Temporales
#25000- 25999 <- Constantes
global_mem_range = [1000,19999]
temp_mem_range = [20001,24999]
const_mem_range = [25000,25999]

class Machine:
    def __init__(self, globals,constants,temporary,cuadruplos):
        
        self.memory=globals
        self.constant =constants
        self.temporary = temporary
        self.instruction_pointer = 0
        self.code = cuadruplos
    def run(self):
        global character_time,character
        while self.instruction_pointer < len(self.code):
            line = self.code[self.instruction_pointer]
            operators = line[1:]
            for value in operators:
                if value != '':
                    if (value >= temp_mem_range[0] and value <= temp_mem_range[1]) and not (value in self.memory):
                        self.memory[value]=self.temporary[value]  
                    elif (value >= const_mem_range[0] and value <= const_mem_range[1]) and not (value in self.memory):
                        self.memory[value]=self.constant[value]
            self.dispatch(line)
            
    def dispatch(self, op):
        dispatch_map = {
            "*":            self.mul,
            "+":            self.plus,
            "-":            self.minus,
            "/":            self.div,
            "==":           self.eq,
            "<>":           self.noteq,
            "arriba":       self.bwd,
            "abajo":        self.fwd,
            "derecha":      self.right,
            "izquierda":    self.left,
            "gotof":        self.gotof,
            "goto":         self.goto,
            "parar":        self.stop,
            "responder":    self.respond,
        }

        if op[0] in dispatch_map:
            dispatch_map[op[0]](op)
        else:
            raise RuntimeError("Unknown opcode: '%s'" % op)

    # OPERATIONS FOLLOW:
    def plus(self,line):
        self.memory[line[3]] = int(self.memory[line[1]]) + int(self.memory[line[2]])
        print(self.memory[line[3]])
        self.instruction_pointer+=1
    def exit(self):
        sys.exit(0)

    def minus(self,line):
        self.memory[line[3]] = int(self.memory[line[1]]) - int(self.memory[line[2]])
        print(self.memory[line[3]])
        self.instruction_pointer+=1
    def mul(self,line):
        self.memory[line[3]] = int(self.memory[line[1]]) * int(self.memory[line[2]])
        print(self.memory[line[3]])
        self.instruction_pointer+=1
    def div(self,line):
        self.memory[line[3]] = int( int(self.memory[line[1]]) / int(self.memory[line[2]]))
        print(self.memory[line[3]])
        self.instruction_pointer+=1
    def stop(self,line):
        self.instruction_pointer+=1
        print("parar")

    def eq(self,line):
        value = self.memory[line[1]]
        if value == "verdadero": value = True
        elif value == "falso": value = False
        objeto = self.memory[line[2]]
        checkforwall = 0
        if objeto[:5] == "pared": checkforwall = 1
        elif objeto[:4] == "meta": checkforwall = 2
        
        if checkforwall < 3:
            if objeto[5:] == "Derecha": objeto = character.isWall(const.right)
            elif objeto[5:] == "Izquierda": objeto = character.isWall(const.left)
            elif objeto[5:] == "Arriba": objeto = character.isWall(const.up)
            elif objeto[5:] == "Abajo": objeto = character.isWall(const.down)
            
            if checkforwall == 0: objeto = not objeto
        else:
            objeto = character.isFinishLine()
        print(objeto)
        print(value)
        if objeto == value: result = True
        else: result = False
        
        print(result)
        self.memory[line[3]] = result
        self.instruction_pointer+=1
    def noteq(self,line):
        #TODO Agregar conexion a interfaz
        return 0

    def gotof(self,line):
        addr=line[3]
        if not self.memory[line[1]]:
            self.instruction_pointer = addr
        else: self.instruction_pointer+=1
        print(self.instruction_pointer)
    def goto(self,line):
        addr=line[3]
        self.instruction_pointer = addr
        
    def bwd(self,line):
        global character
        total = int(self.memory[line[1]])
        while(total > 0):
            character.move(const.up)
            total -=1
        self.instruction_pointer+=1
    def fwd(self,line):
        global character
        total = int(self.memory[line[1]])
        while(total > 0):
            character.move(const.down)
            total -=1
        self.instruction_pointer+=1
    def right(self,line):
        global character
        total = int(self.memory[line[1]])
        while(total > 0):
            character.move(const.right)
            total -=1
        self.instruction_pointer+=1
    def left(self,line):
        global characteer
        total = int(self.memory[line[1]])
        while(total > 0):
            character.move(const.left)
            total -=1
        self.instruction_pointer+=1
    def respond(self,line):
        #TODO Conecion a interfaz para mover personaje
        return 0
    def dump_stack(self):
        print("Data stack (top first):")

        for v in reversed(self.data_stack):
            print(" - type %s, value '%s'" % (type(v), v))


#---------------------Buttons functions--------------------#
    
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
    #TODO Logica para procesar semantica de un programa
    file = open('result.txt','r')
    content = file.read()
    firstPart =content.index('$')
    glob = ast.literal_eval(content[:firstPart])
    content = content[firstPart+1:]
    secondPart =content.index('$')
    const =ast.literal_eval(content[:secondPart])
    content = content[secondPart+1:]
    thirdPart =content.index('$')
    temps =ast.literal_eval(content[:thirdPart])
    content = content[thirdPart+1:]
    code =ast.literal_eval(content)
    a = Machine(glob,const,temps,code)
    a.run()
    print(a.memory)
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
    #TODO Manejar logica de acuerdo al programa escrito
    character.talk(Window,"hello")
def Home():
    global on_game,on_initial,change_button,Label_gen,Frame,execute_button,entryForInput,back_button
    pygame.mixer.music.stop()
    pygame.mixer.music.load(const.musicpath+"Ultralounge.wav")
    #TODO: Activar
    #pygame.mixer.music.play(-1,0.0)
    on_game = False
    on_initial = True
    change_button.kill()
    execute_button.kill()
    back_button.kill()
    Frame.kill()
def Demo():
    pass
    #TODO: Agregar instrucciones
    #para explicar el juego
def Restart():
            global character,Window,list_x2,list_x1,entryForInput
            pygame.time.delay(300)       
        
            for Xil in list_x2:
                Xil.show(Window)
                pygame.display.flip()                     
            mymaze = maze(16, 19)
            mymaze.generate_maze()
            character = Character(mymaze)
            entryForInput.set("")
            while True:
                Window.fill(const.green)
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
def Start_game():
    global on_game,on_initial,Label_gen,Frame,change_button,back_button,execute_button,character_time,entryForInput,character,list_x1,list_x2
    pygame.mixer.music.stop()
    pygame.mixer.music.load(const.musicpath+"Bet_On_It.wav")
    #TODO Activar
    #pygame.mixer.music.play(-1,0.0)
    on_game = True
    on_initial = False
    Frame = StaticFrame(Window, colour = const.Pblue, header = False, bordercolor = const.Pgreen, borderwidth = 5, width = 229, height = 480)
    Frame.place((421, 0))
    #For maze initialization
    mymaze = maze(16, 19)
    mymaze.generate_maze()
    character = Character(mymaze) 
    
    character_time = 0

    list_x1 = list_xil(WW, WH)
    list_x2 = fill_list_x2(list_x1)
    #Pygame directive
    pygame.display.flip()
    pygame.key.set_repeat(50, 55)
    #Side toolbar
    change_button= Button(Window, text = "Cambiar avatar ", width = 95, height = 20, bordercolor = const.Porange, colour = const.yellow, fontsize = 12, target = Change_avatar)
    change_button.place((545, 6))

    Label_gen = Label(Frame, width = 209, height = 290, htitle = " Escribe Aqui ", htitlefont = "Verdana", htitlesize = 14, htitlecolor = Color(const.black[0], const.black[1], const.black[2]), colour = Color(const.Pgreen[0], const.Pgreen[1], const.Pgreen[2]))
    Label_gen.place((10, 20))

    entryForInput = Entry(Frame,width=190,height=270)
    entryForInput.place((15,40))
    #TODO Agregar boton para compilar 
    #y no habilitar boton de ejecutar hasta despues
    execute_button= Button(Window, text = "Correr mi programa! ", width = 145, height = 50, bordercolor = const.Porange, colour = const.yellow, fontsize = 16, target = Execute_instruction)
    execute_button.place((460, 350))
    back_button= Button(Window, text = "Atras ", width = 95, height = 30, bordercolor = const.Porange, colour = const.yellow, fontsize = 12, target = Home)
    back_button.place((460, 420))
# FIN


#---------------------Pygame init--------------------#
pygame.init()


#Window creation
WW, WH = 670, 500
Window = pygame.display.set_mode((WW, WH))
icone = image.load(const.imagespath+avatars[0]+".png")
icone.set_colorkey(const.pink)
pygame.display.set_icon(icone)
pygame.display.set_caption("Xilarius")
pygame.mixer.music.load(const.musicpath+"Ultralounge.wav")
#TODO Activar
#pygame.mixer.music.play(-1,0.0)
# FIN


##Main loop starts
while True:
    pygame.time.Clock().tick(10)
    for event in handle_widgets():
            if event.type == QUIT:
                quit()
                exit()
    if on_game:
        Window.fill(const.green)    
        keys = pygame.key.get_pressed()
        ##TODO: Quitar esto de las teclas
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
            
        ##Blinker for input 
        '''
        currentInput = entryForInput.get()
        if (blinker_on):
          entryForInput.set(currentInput+"|")
          blinker_on =False             
        else:
          entryForInput.set(currentInput.replace('|',''))
          blinker_on = True'''
          
        ##Sets miliseconds between a display loop            
        if pygame.time.get_ticks() - character_time >= const.time_character_poll:
            character_time = pygame.time.get_ticks()
            character.poll()
        character.show(Window)
        render_widgets()
        pygame.display.flip()
        if character.x == character.maze.w - 1 and character.y == character.maze.h - 1:
            Restart()
    elif(on_initial):
        ## Main page
        Window.fill(const.black) 
        start_button= Button(Window, text = "Iniciar! ", width = 95, height = 30, bordercolor = const.Porange, colour = const.yellow, fontsize = 18, target = Start_game)
        start_button.place((545, 6))
		## Background image
        img = image.load(const.imagespath+"Main_Background.png").convert_alpha()
        img.set_colorkey(RLEACCEL)
        rect = Rect((0,0), (0, 0))
        Window.blit(img, rect)
		## Character
        img = image.load(const.imagespath+"Character_boy_Large.png").convert_alpha()
        img.set_colorkey(RLEACCEL)
        rect = Rect((-10,70), (101, 171))
        Window.blit(img, rect)
        ## Bubble message
        img = image.load(const.imagespath+"bubble.png").convert_alpha()
        img.set_colorkey(RLEACCEL)
        rect = Rect((80,20), (101, 171))
        Window.blit(img, rect)
        # TODO Dibujar el resto de la pantalla
        render_widgets()
        pygame.display.flip()
    else:
        #TODO Logica para pantalla de instrucciones
        pass