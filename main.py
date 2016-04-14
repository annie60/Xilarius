# -----------------------------------------------------------------------------
# Interfaz grafica: Xilarius
# Proyecto
# Ana Arellano   		A01089996
# Ana Karen Reyna		A01280310
# -----------------------------------------------------------------------------


#-----------------------Libs import-----------------------#
from __future__ import print_function
import os,webbrowser
import pygame, sys, ast
from pygame.locals import *
from pgu import gui
from time import sleep
from Function import *
from Class import *
from scaner_parser import scan
from tygame.main import StaticFrame,Entry, Button, Label, render_widgets, handle_widgets #But you can put in ..\Python\Lib\site-packages

#-------------------Window Position---------------------#
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (10,150)

#-------------------Global variables---------------------#
avatars = ["Character_boy","Character_Cat_girl",
            "Character_Horn_Girl","Character_Pink_Girl"]
avatar_index=0
main_background = "Main_Background"
on_game = False
on_initial = True
last_position_x =0
last_position_y =0
loop_times =0
execution_errors=[]
can_execute = False
build_error = []
errors = ''
input_initialized = False
input_from_user =""
#------------Virtual Machine---------------#

#Mapeo de memoria
#1000 - 19999 <- Globales
#20000- 24999 <- Temporales
#25000- 25999 <- Constantes
global_mem_range = [1000,19999]
temp_mem_range = [20001,24999]
const_mem_range = [25000,25999]
#Starts all virtual machine functions
class Machine:
    def __init__(self, globals,constants,temporary,cuadruplos):
        
        self.memory=globals
        self.constant =constants
        self.temporary = temporary
        self.instruction_pointer = 0
        self.code = cuadruplos
    def run(self):
        global character_time,character,execution_errors
        
        while self.instruction_pointer < len(self.code) and len(execution_errors) == 0:
            line = self.code[self.instruction_pointer]
            operators = line[1:]
            #Enters the execution case
            for value in operators:
                if value != '':
                    if ((value >= temp_mem_range[0] and value <= temp_mem_range[1])  and not (value in self.memory)):
                            self.memory[value]=self.temporary[value]                        
                    elif (value >= const_mem_range[0] and value <= const_mem_range[1]) and not (value in self.memory):
                        self.memory[value]=self.constant[value]
            self.dispatch(line)
            ##Sets miliseconds between a display loop            
            if pygame.time.get_ticks() - character_time >= const.time_character_poll:
                character_time = pygame.time.get_ticks()
                character.poll()
            character.show(Window)
            render_widgets()
            pygame.display.flip()
            sleep(0.3)
        if(len(execution_errors) > 0):
            Show_execution_errors()
        #TODO Quitar para produccion    
        print(self.memory)
        self.dump_vm()
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
            "exit":         self.exit,
        }

        if op[0] in dispatch_map:
            dispatch_map[op[0]](op)
        else:
            raise RuntimeError("Unknown opcode: '%s'" % op)

    # OPERATIONS FOLLOW:
    def plus(self,line):
        self.memory[line[3]] = int(self.memory[line[1]]) + int(self.memory[line[2]])
        self.instruction_pointer+=1
    def exit(self):
        sys.exit(0)

    def minus(self,line):
        self.memory[line[3]] = int(self.memory[line[1]]) - int(self.memory[line[2]])
        self.instruction_pointer+=1
    def mul(self,line):
        self.memory[line[3]] = int(self.memory[line[1]]) * int(self.memory[line[2]])
        self.instruction_pointer+=1
    def div(self,line):
        self.memory[line[3]] = int( int(self.memory[line[1]]) / int(self.memory[line[2]]))
        self.instruction_pointer+=1
    def stop(self,line):
        self.instruction_pointer+=1

    def eq(self,line):
        value = self.memory[line[1]]
        #Transalte reserved word to instruction
        if value == "verdadero": value = True
        elif value == "falso": value = False
        objeto = self.memory[line[2]]
        #Flag to check for wall or free cell
        checkforwall = 0
        if objeto[:5] == "pared": checkforwall = 1
        elif objeto[:4] == "meta": checkforwall = 2
        #Gets information of the world
        if checkforwall < 3:
            if objeto[5:] == "Derecha": objeto = character.isWall(const.right)
            elif objeto[5:] == "Izquierda": objeto = character.isWall(const.left)
            elif objeto[5:] == "Arriba": objeto = character.isWall(const.up)
            elif objeto[5:] == "Abajo": objeto = character.isWall(const.down)
            #If its not a wall then is checking for 
            #free cell, so negate actual result
            if checkforwall == 0: objeto = not objeto
        else:
            objeto = character.isFinishLine()

        #Makes comparison
        if objeto == value: result = True
        else: result = False
        
        self.memory[line[3]] = result
        self.instruction_pointer+=1
    def noteq(self,line):
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

        if objeto != value: result = True
        else: result = False
        
        self.memory[line[3]] = result
        self.instruction_pointer+=1

    def gotof(self,line):
        addr=line[3]
        if not self.memory[line[1]]:
            self.instruction_pointer = addr
        else: self.instruction_pointer+=1

    def goto(self,line):
        global last_position_x,last_position_y,loop_times,execution_errors
        addr=line[3]
        #Checking for infinite loop
        current_pos_x = character.x
        current_pos_y = character.y
        if current_pos_x == last_position_x and current_pos_y == last_position_y:
            loop_times += 1
        else:
            last_position_x = current_pos_x
            last_position_y = current_pos_y
            loop_times = 0
        if loop_times > 10:
            execution_errors.append("Error: Programa ciclado!")
        else:
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
        Character_talk(self.memory[line[1]])
        self.instruction_pointer+=1
    def dump_vm(self):
        self.memory = {}
# FIN
#---------------------Buttons functions--------------------#
    
##To find solution
def But_path():

    global character

    character.yellow_road = []
    character.reverse = 0
    character.astar(((character.maze.w - 1), (character.maze.h - 1)))
    chemain = character.get_astar((character.x, character.y), ((character.maze.w - 1), (character.maze.h - 1)))
    character.go_to(chemain)
def Compile_instruction():
    global can_execute, build_error,input_from_user
    build_error = scan(input_from_user)
    if not build_error:
        can_execute = True
        errors.set("Exito!")
    else:
        can_execute = False
        Show_production_errors()
 
def Show_execution_errors():
    global execution_errors,errors
    totalerror = 0
    errors.set('')
    for error in execution_errors:
        if totalerror > 3:
            break
        else:
            totalerror += 1
            current_errors = errors.get()
            errors.set(current_errors+error+"\n\n")
def Show_production_errors():
    global execution_errors,errors
    totalerror = 0
    errors.set('')
    for error in build_error:
        if totalerror > 3:
            break
        else:
            totalerror +=1
            current_errors=errors.get()
            errors.set(current_errors+error+"\n\n")
def Execute_instruction():
    global can_execute, build_error,errors
    if can_execute:
        errors.set("Ejecutando tu programa!")
        #Divides file of compiled code
        file = open('result.txt','r')
        content = file.read()
        #Global variables
        firstPart =content.index('$')
        glob = ast.literal_eval(content[:firstPart])
        content = content[firstPart+1:]
        #Constants table
        secondPart =content.index('$')
        const =ast.literal_eval(content[:secondPart])
        content = content[secondPart+1:]
        #Temporals table
        thirdPart =content.index('$')
        temps =ast.literal_eval(content[:thirdPart])
        content = content[thirdPart+1:]
        code =ast.literal_eval(content)
        a = Machine(glob,const,temps,code)
        a.run()
        #TODO Quitar para produccion
        print(a.memory)
        
        errors.set("Termino!")
    else:
        if not build_error:
            build_error.append("No has compilado")
            Show_production_errors()
def Change_avatar():
    global avatar_index,character
    if avatar_index < len(avatars)-1:
        avatar_index+=1
        character.change_avatar(avatars[avatar_index])    
    else:
        avatar_index=0
        character.change_avatar(avatars[avatar_index])
def Character_talk(mensaje):
    global character,Window,character_time
    mensaje_corto = mensaje[1:-1]
    if len(mensaje_corto) > 11:
        mensaje_corto = mensaje_corto[:11]
    character.talk(mensaje_corto)
    if pygame.time.get_ticks() - character_time >= const.time_character_poll:
                character_time = pygame.time.get_ticks()
                character.poll()
    character.show(Window)
    render_widgets()
    pygame.display.flip()
    sleep(2)
    character.stop_talk()
def Home():
    global on_game,on_initial,input_initialized,input_from_user,change_button,Frame,execute_button,back_button, compile_button
    pygame.mixer.music.stop()
    pygame.mixer.music.load(const.musicpath+"Ultralounge.wav")
    #TODO: Activar
    #pygame.mixer.music.play(-1,0.0)
    on_game = False
    on_initial = True
    change_button.kill()
    execute_button.kill()
    compile_button.kill()
    back_button.kill()
    Frame.kill()
    input_initialized = False
    input_from_user = ""
def Demo():
    pass
    #TODO: Agregar instrucciones
    #para explicar el juego
def Restart():
            global character,Window,input_initialized,list_x2,list_x1,input_from_user
            pygame.time.delay(300)       
            
            for Xil in list_x2:
                Xil.show(Window)
                pygame.display.flip()
            #Re generates maze
            mymaze = maze(16, 19)
            mymaze.generate_maze()
            character = Character(mymaze)
            #Cleans variables
            input_from_user = ""
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
            input_initialized = False
def Start_game():
    global on_game,on_initial,input_from_user,Label_gen,Frame,change_button,back_button,execute_button,character_time,entryForInput,character,list_x1,list_x2, compile_button
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
    back_button= Button(Window, text = "Atras", width = 95, height = 20, bordercolor = const.Porange, colour = const.yellow, fontsize = 12, target = Home)
    back_button.place((435, 10))
    change_button= Button(Window, text = "Cambiar avatar ", width = 95, height = 20, bordercolor = const.Porange, colour = const.yellow, fontsize = 12, target = Change_avatar)
    change_button.place((545, 10))

    
    Label_errors = Label(Frame, width = 209, height = 100, htitle = " Estado ", htitlefont = "Verdana", htitlesize = 14, htitlecolor = Color(const.black[0], const.black[1], const.black[2]), colour = Color(const.Pgreen[0], const.Pgreen[1], const.Pgreen[2]))
    Label_errors.place((10, 330))
    global errors
    errors = Entry(Frame,text = "No hay errores ", width=190,height=90)
    errors.place((15,350))
    
    #Buttons
    compile_button= Button(Window, text = "Compilar", width = 95, height = 20, bordercolor = const.Porange, colour = const.yellow, fontsize = 16, target = Compile_instruction)
    compile_button.place((435, 455))
    execute_button= Button(Window, text = "Ejecutar", width = 95, height = 20, bordercolor = const.Porange, colour = const.yellow, fontsize = 16, target = Execute_instruction)
    execute_button.place((545, 455))

def Create_input():
    global Window, input_initialized, Frame, input_from_user
    input_initialized = True 
    app = gui.App(screen = Window,area = Frame)
    app.connect(gui.QUIT,app.quit,None)
    c = gui.Table(width=190,height=270)
    c.tr()
    c.td(gui.Label("    "))
    c.td(gui.Label("    "))
    c.td(gui.Label("    "))
    c.td(gui.Label("    "))
    c.td(gui.Label("    "))
    c.td(gui.Label("    "))
    c.td(gui.Label("    "))
    c.td(gui.Label("    "))
    c.td(gui.Label("    "))
    c.td(gui.Label("    "))
    c.td(gui.Label("    "))
    c.td(gui.Label("    "))
    c.td(gui.Label("    "))
    c.td(gui.Label("    "))
    c.td(gui.Label("    "))
    c.td(gui.Label("    "))
    c.td(gui.Label("    "))
    c.td(gui.Label("    "))
    c.td(gui.Label("    "))
    c.td(gui.Label("    "))
    c.td(gui.Label("    "))
    cancel_btn = gui.Button("Cancelar")
    cancel_btn.connect(gui.CLICK,app.quit,None)
    c.td(cancel_btn)
    
    c.tr()
    c.td(gui.Label("    "))
    c.td(gui.Label("    "))
    c.td(gui.Label("    "))
    c.td(gui.Label("    "))
    c.td(gui.Label("    "))
    c.td(gui.Label("    "))
    c.td(gui.Label("    "))
    c.td(gui.Label("    "))
    c.td(gui.Label("    "))
    c.td(gui.Label("    "))
    c.td(gui.Label("    "))
    c.td(gui.Label("    "))
    c.td(gui.Label("    "))
    c.td(gui.Label("    "))
    c.td(gui.Label("    "))
    c.td(gui.Label("    "))
    c.td(gui.Label("    "))
    c.td(gui.Label("    "))
    c.td(gui.Label("    "))
    c.td(gui.Label("    "))
    c.td(gui.Label("    "))
    def cb():
        global input_from_user
        input_from_user = e.value
        app.quit()
    btn = gui.Button("Guardar")
    btn.connect(gui.CLICK, cb)
    
    c.td(btn)
    c.tr()
    c.td(gui.Label("    "))
    c.td(gui.Label("    "))
    c.td(gui.Label("    "))
    c.td(gui.Label("    "))
    c.td(gui.Label("    "))
    c.td(gui.Label("    "))
    c.td(gui.Label("    "))
    c.td(gui.Label("    "))
    c.td(gui.Label("    "))
    c.td(gui.Label("    "))
    c.td(gui.Label("    "))
    c.td(gui.Label("    "))
    c.td(gui.Label("    "))
    c.td(gui.Label("    "))
    c.td(gui.Label("    "))
    c.td(gui.Label("    "))
    c.td(gui.Label("    "))
    c.td(gui.Label("    "))
    c.td(gui.Label("    "))
    c.td(gui.Label("    "))
    c.td(gui.Label("    "))
    if input_from_user == "":
        previous_text = "miPrograma Uno;\n{\ncrearPersonaje Nombre;\nNombre.abajo(1);\n}"
    else:
        previous_text = input_from_user
    e = gui.TextArea(value=previous_text,width=250,height=270)
    c.td(e)

    app.run(c)
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
        mouse = pygame.mouse.get_pressed()
        if mouse[0]:
            (mousex,mousey) = pygame.mouse.get_pos()
            if mousex > 445 and mousex < 630:
                if mousey > 60 and mousey < 325:
                    input_initialized = False
        '''
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
                Character_talk("'hola'")
        '''
        Label_gen = Label(Frame, width = 209, height = 290, htitle = " Programa ", htitlefont = "Verdana", htitlesize = 14, htitlecolor = Color(const.black[0], const.black[1], const.black[2]), colour = Color(const.Pgreen[0], const.Pgreen[1], const.Pgreen[2]))
        Label_gen.place((10, 30))

        entryForInput = Entry(Frame,width=190,height=270)
        entryForInput.place((15,50))
        entryForInput.set(str(input_from_user))
        ##Sets miliseconds between a display loop            
        if pygame.time.get_ticks() - character_time >= const.time_character_poll:
            character_time = pygame.time.get_ticks()
            character.poll()
        character.show(Window)
        if not input_initialized:
            Create_input()
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