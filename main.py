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
from scaner_parser import Scanner
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
executing = False
input_file = gui.Input()
last_position_x =0
last_position_y =0
loop_times =0
execution_errors=[]
can_execute = False
build_error = []
errors = ''
used_help = False
input_initialized = False
input_from_user =""
easy_maze =[10,13]
hard_maze = [16,19]
dificulty_level = 1

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
        global character,execution_errors
        ##While there is code to run and there is no error and the character hasn't arrive to the finish line
        while self.instruction_pointer < len(self.code) and len(execution_errors) == 0 and not character.isFinishLine(character.x,character.y):
            line = self.code[self.instruction_pointer]
            operators = line[1:]
            #Enters the execution case
            for value in operators:
                if value != '':
                    if ((value >= temp_mem_range[0] and value <= temp_mem_range[1])  and not (value in self.memory)):
                        self.memory[value]=self.temporary[value]                        
                    elif (value >= const_mem_range[0] and value <= const_mem_range[1]) and not (value in self.memory):
                        self.memory[value]=self.constant[value]
                    elif not (value in self.memory) and (value > const_mem_range[1] or value > temp_mem_range[1]):
                        execution_errors.append("Error: Falta de memoria.")
            if len(execution_errors) == 0 :
                self.dispatch(line)
                Update_display()
                sleep(0.1)
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
            "=":            self.assign,
            "==":           self.eq,
            "<>":           self.noteq,
            "no":           self.negative,
            "hacerEscrita": self.convert,
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
    def assign(self,line):
        self.memory[line[2]]= self.memory[line[1]]
        self.instruction_pointer+=1
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
        if checkforwall < 2:
            if objeto[5:] == "Derecha": objeto = character.isWall(const.right)
            elif objeto[5:] == "Izquierda": objeto = character.isWall(const.left)
            elif objeto[5:] == "Arriba": objeto = character.isWall(const.up)
            elif objeto[5:] == "Abajo": objeto = character.isWall(const.down)
            #If its not a wall then is checking for 
            #free cell, so negate actual result
            if checkforwall == 0: objeto = not objeto
        else:
            if objeto[4:] == "Derecha": objeto = character.isFinishLine(character.x+1,character.y)
            elif objeto[4:] == "Izquierda": objeto = character.isFinishLine(character.x-1,character.y)
            elif objeto[4:] == "Arriba": objeto = character.isFinishLine(character.x,character.y+1)
            elif objeto[4:] == "Abajo": objeto = character.isFinishLine(character.x,character.y-1)
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
        #Translates directive
        if checkforwall < 3:
            if objeto[5:] == "Derecha": objeto = character.isWall(const.right)
            elif objeto[5:] == "Izquierda": objeto = character.isWall(const.left)
            elif objeto[5:] == "Arriba": objeto = character.isWall(const.up)
            elif objeto[5:] == "Abajo": objeto = character.isWall(const.down)
            
            if checkforwall == 0: objeto = not objeto
        else:
            if objeto[4:] == "Derecha": objeto = character.isFinishLine(character.x+1,character.y)
            elif objeto[4:] == "Izquierda": objeto = character.isFinishLine(character.x-1,character.y)
            elif objeto[4:] == "Arriba": objeto = character.isFinishLine(character.x,character.y+1)
            elif objeto[4:] == "Abajo": objeto = character.isFinishLine(character.x,character.y-1)

        if objeto != value: result = True
        else: result = False
        
        self.memory[line[3]] = result
        self.instruction_pointer+=1
    def negative(self,line):
        self.memory[line[3]]= not self.memory[line[1]]
        self.instruction_pointer+=1
    def convert(self,line):
        self.memory[line[3]]= '"'+str(self.memory[line[1]])+'"'
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
        #Checks if the current position hasn't change for over 10 cycles
        #if it hasn't then it's consider to be on an infinite loop.
        if current_pos_x == last_position_x and current_pos_y == last_position_y:
            loop_times += 1
        elif current_pos_x == (last_position_x -1) or current_pos_y == (last_position_y-1):
            loop_times += 1
        else:
            last_position_x = current_pos_x
            last_position_y = current_pos_y
            loop_times = 0
        if loop_times > 10:
            execution_errors.append("Error: Programa ciclado!")
        else:
            self.instruction_pointer = addr
        sleep(0.05)
    def bwd(self,line):
        global character
        total = int(self.memory[line[1]])
        while(total > 0):
            character.move(const.up)
            Update_display()
            sleep(0.05)
            total -=1
        self.instruction_pointer+=1
    def fwd(self,line):
        global character
        total = int(self.memory[line[1]])
        while(total > 0):
            character.move(const.down)
            Update_display()
            sleep(0.05)
            total -=1
        self.instruction_pointer+=1
    def right(self,line):
        global character
        total = int(self.memory[line[1]])
        while(total > 0):
            character.move(const.right)
            Update_display()
            sleep(0.05)
            total -=1
        self.instruction_pointer+=1
    def left(self,line):
        global characteer
        total = int(self.memory[line[1]])
        while(total > 0):
            character.move(const.left)
            Update_display()
            sleep(0.05)
            total -=1
        self.instruction_pointer+=1
    def respond(self,line):
        Character_talk(self.memory[line[1]])
        self.instruction_pointer+=1
    def dump_vm(self):
        self.memory = {}
# FIN
#---------------------Buttons functions--------------------#
    
def But_path():
    global character,input_from_user
    character.yellow_road = []
    character.reverse = 0
    line_counter = 0
    character.astar(((character.maze.w - 1), (character.maze.h - 1)))
    #Checks for previous written input from user
    if len(input_from_user) > 0:
        input_from_user = ""
        
    del const.instructions[:]
    #Gets path to follow
    road = character.get_astar((character.x, character.y), ((character.maze.w - 1), (character.maze.h - 1)))
    #Creates input from the solution found.
    for instruction in const.instructions:
        temp_entry = input_from_user
        input_from_user = temp_entry+instruction+"\n"
        line_counter += 1
    render_widgets()
    character.go_to(road)
def Compile_instruction():
    global can_execute, loop_times,build_error,input_from_user,executing,executing_errors
    scanner = Scanner(input_from_user)
    build_error = scanner.scan()
    ##Checks if there is not a previous instance running
    if not build_error and not executing:
        can_execute = True
        errors.set("Exito!")
        del execution_errors[:]
        loop_times = 0
    elif(build_error and not executing):
        can_execute = False
        Show_production_errors()
        #Destroy build errors each time its called
        del build_error[:]
        del execution_errors[:]
        loop_times = 0
 
def Show_execution_errors():
    global execution_errors,errors
    totalerror = 0
    errors.set('')
    for error in execution_errors:
        if totalerror > 7:
            break
        else:
            totalerror += 1
            current_errors = errors.get()
            errors.set(current_errors+error+"\n")
            
def Show_production_errors():
    global execution_errors,errors
    totalerror = 0
    errors.set('')
    for error in build_error:
        #Only produces 7 since the entry doesn't have scroll
        if totalerror > 7:
            break
        else:
            totalerror +=1
            current_errors=errors.get()
            errors.set(current_errors+error+"\n")
def Update_display():
    global character,character_time,Window
    ##Sets miliseconds between a display loop            
    if pygame.time.get_ticks() - character_time >= const.time_character_poll:
        character_time = pygame.time.get_ticks()
        character.poll()
    character.show(Window)
    render_widgets()
    pygame.display.flip()
def Execute_instruction():
    global can_execute, build_error,errors, executing, execution_Error
    if can_execute and not executing:
        errors.set("Ejecutando tu programa!")
        executing = True
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
        executing = False
        if len(execution_errors) == 0:
            errors.set("Termino!")
    elif(not can_execute and not executing):
        if not build_error:
            build_error.append("No has compilado correctamente")
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
    global character,Window
    #Formats message so it can fit on the bubble
    mensaje_corto = mensaje[1:-1]
    if len(mensaje_corto) > 11:
        mensaje_corto = mensaje_corto[:11]
    character.talk(mensaje_corto)
    Update_display()
    sleep(2)
    character.stop_talk()
    
def Complete_cleanup(all):
    global can_execute,executing,avatar_index,on_game,input_from_user,build_error,execution_errors,loop_times,input_from_user,input_initialized,used_help
    can_execute = False
    loop_times =0
    used_help = False
    del build_error[:]
    del execution_errors[:]
    executing = False
    avatar_index=0
    if all == 0:
        input_from_user = ""
    input_initialized = False
def Home():
    global on_game,executing,on_initial,change_button,Frame,execute_button,back_button, compile_button,dificulty_level
    if not executing:
        dificulty_level = 1
        pygame.mixer.music.stop()
        pygame.mixer.music.load(const.musicpath+"Ultralounge.wav")
        #TODO: Activar
        #pygame.mixer.music.play(-1,0.0)
        on_game = False
        on_initial = True
        #Clears display
        change_button.kill()
        execute_button.kill()
        compile_button.kill()
        back_button.kill()
        Frame.kill()
        Complete_cleanup(0)

def Restart():
            global character,used_help,Window,input_initialized,list_x2,list_x1,input_from_user
            pygame.time.delay(300)       
            #Avatar wall displayed on the screen
            for Xil in list_x2:
                Xil.show(Window)
                pygame.display.flip()
            #Re generates maze
            if dificulty_leve == 1:
                mymaze = maze(easy_maze[0],easy_maze[1])
            else:
                mymaze = maze(hard_maze[0],hard_maze[1])
            mymaze.generate_maze()
            character = Character(mymaze)
            
            #Checks if there was use of help on the last game
            if used_help:
                #Cleans variables
                Complete_cleanup(1)
            else:
                #Cleans variables
                Complete_cleanup(0)
            #Creates solution for the new maze
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
    global on_game,can_execute,on_initial,input_from_user,Label_gen,Frame,change_button,back_button,execute_button,character_time,entryForInput,character,list_x1,list_x2, compile_button
    #Load background music
    pygame.mixer.music.stop()
    pygame.mixer.music.load(const.musicpath+"Bet_On_It.wav")
    #TODO Activar
    #pygame.mixer.music.play(-1,0.0)
    on_game = True
    on_initial = False
    Frame = StaticFrame(Window, colour = const.Pblue, header = False, bordercolor = const.Pgreen, borderwidth = 5, width = 235, height = 485)
    can_execute = False
    Frame.place((421, 0))
    #For maze initialization
    if dificulty_level == 1:
        mymaze = maze(easy_maze[0],easy_maze[1])
    else:
        mymaze = maze(hard_maze[0],hard_maze[1])
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

    #Errors output section
    Label_errors = Label(Frame, width = 209, height = 110, htitle = " Estado ", htitlefont = "Verdana", htitlesize = 14, htitlecolor = Color(const.black[0], const.black[1], const.black[2]), colour = Color(const.Pgreen[0], const.Pgreen[1], const.Pgreen[2]))
    Label_errors.place((10, 330))
    global errors
    errors = Entry(Frame,text = "No hay errores ",textcolor=Color("Red"), width=195,height=90,fontsize=11)
    errors.place((15,350))
    
    #Buttons
    compile_button= Button(Window, text = "Compilar", width = 95, height = 20, bordercolor = const.Porange, colour = const.yellow, fontsize = 16, target = Compile_instruction)
    compile_button.place((435, 460))
    execute_button= Button(Window, text = "Ejecutar", width = 95, height = 20, bordercolor = const.Porange, colour = const.yellow, fontsize = 16, target = Execute_instruction)
    execute_button.place((545, 460))
    
def Expert_mode():
    global dificulty_level
    dificulty_level = 2
    Start_game()
def open_file_browser():
    d = gui.FileDialog()
    d.connect(gui.CHANGE, handle_file_browser_closed, d)
    d.open()
    
def handle_file_browser_closed(dlg):
    global input_from_user
    if dlg.value: input_file.value = dlg.value
    if '.txt' in input_file.value:
        file = open(input_file.value,'r')
        content = file.read()
        content.replace('\n','\n\n')
        input_from_user = content

def Create_input():
    global Window, input_initialized,can_execute, Frame, input_from_user
    input_initialized = True

    #App over toolbar
    app = gui.App(screen = Window,area = Frame)
    app.connect(gui.QUIT,app.quit,None)
    my_container1 = gui.Container(width =670,height = 500)

    #Cancel button
    cancel_btn = gui.Button("Cancelar")
    cancel_btn.connect(gui.CLICK,app.quit,None)
    #To save current input on the display
    def cb():
        global input_from_user,can_execute
        input_from_user = e.value
        can_execute = False
        app.quit()

    #Save button
    btn = gui.Button("Guardar")
    btn.connect(gui.CLICK, cb)
    #Checks for previous program
    if input_from_user == "":
        previous_text = "miPrograma Uno;\n{\ncrearPersonaje Nombre;\nvar Mi numero = 3;\nMi = 5;\nNombre.abajo(1);\n}"
    else:
        previous_text = input_from_user
    e = gui.TextArea(value=previous_text,width=250,height=360)

    def help():
        global Window,Frame,input_from_user
        #Saves changes on the input
        input_from_user = e.value
        #App over toolbar
        second_app = gui.Desktop(screen = Window,area = Frame)
        my_container2 = gui.Container(width =670,height = 500)
        second_app.connect(gui.QUIT,second_app.quit,None)
        second_app.connect(gui.QUIT,app.quit,None)
        #Exit button
        cancel_btn = gui.Button("Salir")
        cancel_btn.connect(gui.CLICK,second_app.quit,None)
        cancel_btn.connect(gui.CLICK,app.quit,None)
        #Add items to container
        my_container2.add(gui.Image(const.imagespath+"Instrucciones_Background.png"),0,0)
        my_container2.add(cancel_btn,610,10)
        second_app.run(my_container2)
        pygame.display.flip()

    #Help button
    btn_help = gui.Button("Instrucciones")
    btn_help.connect(gui.CLICK, help)
    def file_treat():
        global Window,Frame
        third_app = gui.Desktop(screen = Window,area = Frame)
        third_app.connect(gui.QUIT,third_app.quit,None)
        third_app.connect(gui.QUIT,app.quit,None)
        my_container3 = gui.Container(width =670,height = 500)
        open_btn = gui.Button("Abrir")
        open_btn.connect(gui.CLICK,open_file_browser,None)
        my_container3.add(open_btn,300,200)
        third_app.run(my_container3)
        pygame.display.flip()
    
    #file treatment
    btn_file = gui.Button("Archivo")
    btn_file.connect(gui.CLICK,file_treat)
    
    #Add items to container
    my_container1.add(cancel_btn,500,20)
    my_container1.add(btn,502,50)
    my_container1.add(btn_file,595,20)
    my_container1.add(e,416,80)
    my_container1.add(btn_help,480,460)
    app.run(my_container1) 
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
#----------------------------------------------#
while True:
    pygame.time.Clock().tick(10)
    for event in handle_widgets():
            if event.type == QUIT:
                quit()
                exit()
    if on_game:
        Window.fill(const.green)
        keys = pygame.key.get_pressed()
        #Keyboard help finding solution
        if keys:
            if keys[K_h] and not executing:
                But_path()
                used_help =True
        ##Mouse events for the input detection
        mouse = pygame.mouse.get_pressed()
        if mouse[0] and not executing :
            (mousex,mousey) = pygame.mouse.get_pos()
            if mousex > 445 and mousex < 630:
                if mousey > 60 and mousey < 325:
                    input_initialized = False
                    can_execute = False
        #Second set of widgets
        Label_gen = Label(Frame, width = 220, height = 290, htitle = " Programa ", htitlefont = "Verdana", htitlesize = 14, htitlecolor = Color(const.black[0], const.black[1], const.black[2]), colour = Color(const.Pgreen[0], const.Pgreen[1], const.Pgreen[2]))
        Label_gen.place((3, 30))
        #Widget for line counter
        entry_line_no = Entry(Frame,width=15,height=270,textcolor = Color("blue"),bold=True)
        entry_line_no.place((5,50))
        line_no = ""
        for value in range(1,50):
            line_no = line_no+str(value)+"\n\n"
        entry_line_no.set(line_no)
        #Visual of current code , non editable
        entryForInput = Entry(Frame,width=195,height=270)
        entryForInput.place((20,50))
        input_formatted = str(input_from_user)
        input_formatted = input_formatted.replace("\n","\n\n")
        entryForInput.set(input_formatted)
        ##Sets miliseconds between a display loop            
        if pygame.time.get_ticks() - character_time >= const.time_character_poll:
            character_time = pygame.time.get_ticks()
            character.poll()
        ##Renders rest of display
        character.show(Window)
        if not input_initialized:
            Create_input()
        render_widgets()
        pygame.display.flip()
        #If the character is on the finish line
        if character.x == character.maze.w - 1 and character.y == character.maze.h - 1:
            Restart()
        
    elif(on_initial):
        ## Main page
        Window.fill(const.black)
        start_button= Button(Window, text = "Iniciar! ", width = 95, height = 30, bordercolor = const.Porange, colour = const.yellow, fontsize = 18, target = Start_game)
        start_button.place((565, 6))
        expert_button= Button(Window, text = "Modo Experto! ", width = 120, height = 30, bordercolor = const.white, colour = const.red, fontsize = 16, target = Expert_mode)
        expert_button.place((540, 70))
	## Background image
        img = image.load(const.imagespath+"Main_Background.png").convert_alpha()
        img.set_colorkey(RLEACCEL)
        rect = Rect((0,0), (0, 0))
        Window.blit(img, rect)
        ## Character
        img = image.load(const.imagespath+"Character_boy_Large.png").convert_alpha()
        img.set_colorkey(RLEACCEL)
        rect = Rect((-10,115), (101, 171))
        Window.blit(img, rect)
        ## Bubble message
        img = image.load(const.imagespath+"bubble.png").convert_alpha()
        img.set_colorkey(RLEACCEL)
        rect = Rect((75,70), (101, 171))
        Window.blit(img, rect)
        render_widgets()
        pygame.display.flip()