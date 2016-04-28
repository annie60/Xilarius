# -----------------------------------------------------------------------------
# Virtual machine and graphic interface: Xilarius
# Project
# Ana Arellano   		A01089996
# Ana Karen Reyna		A01280310
# -----------------------------------------------------------------------------


'''-----------------------Libs import-----------------------'''
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

'''-------------------Window Position---------------------'''
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (10,150)

'''-------------------Global variables---------------------'''
avatars = ["Character_boy","Character_Cat_girl",
            "Character_Horn_Girl","Character_Pink_Girl"]
avatar_index=0
main_background = "Main_Background"
on_game = False
on_initial = True
correct_message=["Perfecto! Tu programa esta listo","Excelente!,ahora paso 2","Muy bien! Ahora a probarlo.","Genial! Es turno del paso 2"]
executing = False
input_file = gui.Input()
last_position_x =0
last_position_y =0
loop_times =0
score = 0
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
running = True
numero_hint = 1
#Table for score points
# expresion (+ / * -) +1
# condition +5
# assign + 1
# loop + 8
# function + 1
# negative + 3
# convert +4

#------------Virtual Machine---------------#

#Memory map
#1000 - 19999 <- Globals
#20000- 24999 <- Temporals
#25000- 25999 <- Constants
global_mem_range = [1000,19999]
temp_mem_range = [20000,24999]
const_mem_range = [25000,25999]
'''--------------Virtual machine functions----------------'''
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
            #Pause event from the keyboard
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        Stop()
            operators = line[1:]
            #Enters the execution case
            for value in operators:
                if value != '':
                    if ((value >= temp_mem_range[0] and value <= temp_mem_range[1])  and not (value in self.memory)):
                        self.memory[value]=self.temporary[value]                        
                    elif (value >= const_mem_range[0] and value <= const_mem_range[1]) and not (value in self.memory):
                        self.memory[value]=self.constant[value]
                    elif not (value in self.memory) and (value > const_mem_range[1] or value > temp_mem_range[1]):
                        execution_errors.append("Error: Ya no hay memoria.")
            #If there where no errors then continues the dispatch
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
        global score
        score +=1
        self.memory[line[3]] = int(self.memory[line[1]]) + int(self.memory[line[2]])
        self.instruction_pointer+=1
    def exit(self):
        sys.exit(0)
    def assign(self,line):
        global score
        score +=1
        self.memory[line[2]]= self.memory[line[1]]
        self.instruction_pointer+=1
    def minus(self,line):
        global score
        score +=1
        self.memory[line[3]] = int(self.memory[line[1]]) - int(self.memory[line[2]])
        self.instruction_pointer+=1
    def mul(self,line):
        global score
        score +=1
        self.memory[line[3]] = int(self.memory[line[1]]) * int(self.memory[line[2]])
        self.instruction_pointer+=1
    def div(self,line):
        global score
        score +=1
        self.memory[line[3]] = int( int(self.memory[line[1]]) / int(self.memory[line[2]]))
        self.instruction_pointer+=1
    def stop(self,line):
        global score
        score +=1
        self.instruction_pointer+=1
    def translate(self,value,objeto):
        #Transalte reserved word to instruction
        if value == "verdadero": value = True
        elif value == "falso": value = False
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
        return result
    def eq(self,line):
        value = self.memory[line[1]]
        object = self.memory[line[2]]
        result = self.translate(value,object)
        self.memory[line[3]] = result
        self.instruction_pointer+=1
    def noteq(self,line):
        value = self.memory[line[1]]
        object = self.memory[line[2]]
        result = self.translate(value,object)
        self.memory[line[3]] = not result
        self.instruction_pointer+=1
    def negative(self,line):
        global score
        score +=3
        self.memory[line[3]]= not self.memory[line[1]]
        self.instruction_pointer+=1
    def convert(self,line):
        global score
        score +=4
        self.memory[line[3]]= '"'+str(self.memory[line[1]])+'"'
        self.instruction_pointer+=1
    def gotof(self,line):
        global score
        score +=5
        addr=line[3]
        if not self.memory[line[1]]:
            self.instruction_pointer = addr
        else: self.instruction_pointer+=1

    def goto(self,line):
        global score
        score +=8
        global last_position_x,last_position_y,loop_times,execution_errors
        addr=line[3]
        #Checking for infinite loop
        current_pos_x = character.x
        current_pos_y = character.y
        #Checks if the current position hasn't change for over 10 cycles
        #if it hasn't then it's consider to be on an infinite loop.
        if current_pos_x == last_position_x and current_pos_y == last_position_y:
            loop_times += 1
        #Checks if the position is changing just between two points
        #if its then is getting cycle
        elif current_pos_x == (last_position_x -1) or current_pos_y == (last_position_y-1):
            loop_times += 1
        else:
            last_position_x = current_pos_x
            last_position_y = current_pos_y
            loop_times = 0
        if loop_times > 10:
            execution_errors.append("Oh oh hubo un error")
            execution_errors.append("El programa se ciclo!")
            score = 0
        else:
            self.instruction_pointer = addr
        sleep(0.05)
    def bwd(self,line):
        global score
        score +=1
        global character
        total = int(self.memory[line[1]])
        #Executes action as many times as the user indicated
        while(total > 0):
            character.move(const.up)
            Update_display()
            sleep(0.05)
            total -=1
        self.instruction_pointer+=1
    def fwd(self,line):
        global score
        score +=1
        global character
        total = int(self.memory[line[1]])
        #Executes action as many times as the user indicated
        while(total > 0):
            character.move(const.down)
            Update_display()
            sleep(0.05)
            total -=1
        self.instruction_pointer+=1
    def right(self,line):
        global score
        score +=1
        global character
        total = int(self.memory[line[1]])
        #Executes action as many times as the user indicated
        while(total > 0):
            character.move(const.right)
            Update_display()
            sleep(0.05)
            total -=1
        self.instruction_pointer+=1
    def left(self,line):
        global score
        score +=1
        global characteer
        total = int(self.memory[line[1]])
        #Executes action as many times as the user indicated
        while(total > 0):
            character.move(const.left)
            Update_display()
            sleep(0.05)
            total -=1
        self.instruction_pointer+=1
    def respond(self,line):
        global score
        score +=1
        Character_talk(self.memory[line[1]])
        self.instruction_pointer+=1
    def dump_vm(self):
        self.memory = {}

'''---------------------Buttons functions--------------------'''
  
def But_path():#Generates solution and solves current maze  
    global character,input_from_user
    character.yellow_road = []
    character.reverse = 0
    line_counter = 0
    #Gets where the goal is
    character.goal(((character.maze.w - 1), (character.maze.h - 1)))
    #Checks for previous written input from user
    if len(input_from_user) > 0:
        input_from_user = ""
        
    del const.instructions[:]
    #Gets path to follow
    road = character.get_goal((character.x, character.y), ((character.maze.w - 1), (character.maze.h - 1)))
    #Creates input from the solution found.
    for instruction in const.instructions:
        temp_entry = input_from_user
        input_from_user = temp_entry+instruction+"\n"
        line_counter += 1
    render_widgets()
    #Moves character accordingly
    character.go_to(road)

def Compile_instruction():#Compiles current code as input from user
    global can_execute,correct_message,loop_times,build_error,input_from_user,executing,executing_errors
    ##Checks if there is not a previous instance running
    if not executing:
        scanner = Scanner(input_from_user)
        build_error = scanner.scan()
        #Checks if there where any compilation errors
        if not build_error:
            can_execute = True
            errors.set(correct_message[randint(0,3)])
            loop_times = 0
        else:
            can_execute = False
            Show_production_errors()
            #Destroy build errors each time its called
            del build_error[:]
            loop_times = 0
        #Destroy exection errors each time its called
        del execution_errors[:]

def Show_execution_errors():#Shows execution errors generated on the compilation
    global execution_errors,errors
    totalerror = 0
    errors.set('')
    final_errors=""
    for error in execution_errors:
        if totalerror > 7:
            break
        else:
            totalerror += 1
            final_errors = final_errors+error+"\n"
    errors.set(final_errors)
           
def Show_production_errors():#Displays mistakes produced while running the application 
    global execution_errors,errors
    totalerror = 0
    errors.set('')
    final_errors=""
    for error in build_error:
        #Only produces 7 since the entry doesn't have scroll
        if totalerror > 7:
            break
        else:
            totalerror +=1
            final_errors = final_errors+error+"\n"
            
    errors.set(final_errors)

def Update_display():#Re renders objects on the screen with the changes made on the values
    global character,character_time,Window,entry_score
    ##Sets miliseconds between a display loop            
    if pygame.time.get_ticks() - character_time >= const.time_character_poll:
        character_time = pygame.time.get_ticks()
        character.poll()
    character.show(Window)
    entry_score.set("Puntos:"+str(score))
    render_widgets()
    pygame.display.flip()

def Execute_instruction():#Executes the intermediate code generated previously
    global can_execute, loop_times,build_error,errors, executing, execution_Error
    #If there where no mistakes during compilation and there is no
    #previous instance running then continue
    if can_execute and not executing:
        errors.set("Ejecutando tu programa!\nPsst ve como Xilarius se mueve!")
        #Flag to disable any other feature meanwhile the program executes
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
            errors.set("Tu programa termino!")
            loop_times = 0
    elif(not can_execute and not executing):
        #If there are no errors but it can't execute then if means
        #it hasn't been compile
        if not build_error:
            build_error.append("Ups! No has hecho el paso uno")
            Show_production_errors()
            del build_error[:]
           
def Change_avatar():#Gets another image to display as the avatar 
    global avatar_index,character
    if avatar_index < len(avatars)-1:
        avatar_index+=1
        character.change_avatar(avatars[avatar_index])    
    else:
        avatar_index=0
        character.change_avatar(avatars[avatar_index])
      
def Character_talk(mensaje):#Handles the use of character's dialog  
    global character,Window
    #Formats message so it can fit on the bubble
    short_message = mensaje[1:-1]
    if len(short_message) > 11:
        short_message = short_message[:11]
    character.talk(short_message)
    Update_display()
    sleep(1)
    character.stop_talk()
  
def Complete_cleanup(all):#Cleans all variables used on the session  
    global can_execute,score,executing,avatar_index,on_game,input_from_user,build_error,execution_errors,loop_times,input_from_user,input_initialized,used_help
    can_execute = False
    loop_times =0
    used_help = False
    del build_error[:]
    del execution_errors[:]
    executing = False
    score =0
    avatar_index=0
    if all == 0:
        input_from_user = ""
    input_initialized = False

def Home():#Renders initial screen for the game when return from an instance of the game
    global on_game,executing,on_initial,change_button,Frame,execute_button,home_button, compile_button,dificulty_level,exit_button
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
        home_button.kill()
        Frame.kill()
        exit_button.kill()
        Complete_cleanup(0)

def Exit():
    global running
    running = False

def Restart():#Creates new instance of the game with the same dificulty 
            global character,score,dificulty_level,used_help,Window,list_x2,list_x1
            pygame.time.delay(300)
            #Total score message
            img = image.load(const.imagespath+"bubble_large.png").convert_alpha()
            img.set_colorkey(RLEACCEL)
            rect = Rect((80,75), (125, 200))
            Window.blit(img,rect)
            font = pygame.font.Font(None, 36)
            text = font.render("Total de puntos: "+str(score), 1, const.red)
            textpos = Rect((150,145),(165,235))
            Window.blit(text, textpos)
            #If the score is too low sends game over message else says its completed
            if(score < 200):
                text = font.render("Intenta de nuevo", 1, Color(1,72,152))
                textpos = Rect((175,180),(175,245))
                Window.blit(text, textpos)
            else:
                text = font.render("Muy bien!Prueba con experto", 1, Color(1,72,152))
                textpos = Rect((175,180),(175,245))
                Window.blit(text, textpos)
            pygame.display.flip()
            sleep(3.5)
            #Avatar wall displayed on the screen
            for Xil in list_x2:
                Xil.show(Window)
                pygame.display.flip()
            #Re generates maze
            if dificulty_level == 1:
                mymaze = maze(easy_maze[0],easy_maze[1])
            else:
                mymaze = maze(hard_maze[0],hard_maze[1])
            mymaze.generate_maze()
            character = Character(mymaze)

            #Checks if there was use of help on the last game
            if used_help:
                #Cleans variables with exeption of code generated
                Complete_cleanup(1)
            else:
                #Cleans variables completly
                Complete_cleanup(0)
            #To remove the wall of avatars
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
            
          
def Start_game():#Initialize game's screen and its controlers  
    global on_game,can_execute,on_initial,input_from_user,Label_gen,Frame,change_button,home_button,execute_button,character_time,entryForInput,character,list_x1,list_x2, compile_button,exit_button
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
    home_button= Button(Window, text = "Inicio", width = 50, height = 20, bordercolor = const.Porange, colour = const.yellow, fontsize = 12, target = Home)
    home_button.place((430, 10))
    change_button= Button(Window, text = "  Cambiar avatar ", width = 80, height = 20, bordercolor = const.Porange, colour = const.yellow, fontsize = 11, target = Change_avatar)
    change_button.place((500, 10))
    exit_button= Button(Window, text = "Salir", width = 50, height = 20, bordercolor = const.white, colour = const.red, fontsize = 12, target = Exit)
    exit_button.place((600, 10))

    #Errors output section
    Label_errors = Label(Frame, width = 220, height = 110, htitle = " Estado ", htitlefont = "Verdana", htitlesize = 14, htitlecolor = Color(const.black[0], const.black[1], const.black[2]), colour = Color(const.Pgreen[0], const.Pgreen[1], const.Pgreen[2]))
    Label_errors.place((7, 330))
    global errors
    errors = Entry(Frame,text = "No hay errores ",textcolor=Color("Red"), width=206,height=90,fontsize=11)
    errors.place((12,350))
    
    #Buttons
    compile_button= Button(Window, text = "Paso 1", width = 95, height = 20, bordercolor = const.white, colour = const.Porange, fontsize = 16, target = Compile_instruction)
    compile_button.place((435, 460))
    execute_button= Button(Window, text = "Paso 2", width = 95, height = 20, bordercolor = const.white, colour = const.green, fontsize = 16, target = Execute_instruction)
    execute_button.place((545, 460))
def Stop():
    global execution_errors
    execution_errors.append("Detenido")
def Expert_mode():#Change dificulty level and calls to start game  
    global dificulty_level
    dificulty_level = 2
    Start_game()
'''-----------------File treatment section--------------------'''
def open_file_browser(mode):
    d = gui.FileDialog()
    d.connect(gui.CHANGE, handle_file_browser_closed, d,mode)
    d.open()
    
def handle_file_browser_closed(dlg,write):
    global input_from_user
    file_name = input_file.value
    if dlg.value: file_name = dlg.value
    #Checks if its to write or read a file
    if ('.txt' in file_name) and write:
        file = open(file_name,'r')
        content = file.read()
        content.replace('\n','\n\n')
        input_from_user = content
    else:
        file = open(file_name,'w')
        input_from_user = input_from_user.replace('\n\n','\n')
        file.write(input_from_user)
def Create_input():#Opens screen to handle text input from the user
    global Window, input_initialized,can_execute, Frame, input_from_user
    input_initialized = True
    
    #App over toolbar
    app = gui.App(screen = Window,area = Frame)
    app.connect(gui.QUIT,app.quit,None)
    my_container1 = gui.Container(width =670,height = 500)

    #Label to write code
    Label_code = gui.Label("Escribe/modifica tu código:")
    #Label to buttons
    Label_buttons = gui.Label("Cambios realizados:")

    #Cancel button
    cancel_btn = gui.Button("Cancelar")
    cancel_btn.connect(gui.CLICK,app.quit,None)
    #To save current input on the display
    def cb():
        global input_from_user,can_execute
        input_from_user = textarea_code.value
        can_execute = False
        app.quit()

    #Save button
    save_btn = gui.Button("Guardar")
    save_btn.connect(gui.CLICK, cb)
    #Checks for previous program
    if input_from_user == "":
        previous_text = "miPrograma Uno;\n{\ncrearPersonaje Nombre;\nvar Mi numero = 3;\nMi = 5;\nNombre.abajo(1);\n}"
    else:
        previous_text = input_from_user
    textarea_code = gui.TextArea(value=previous_text,width=235,height=360)

    def help():
        global Window,Frame,input_from_user
        #Saves changes on the input
        input_from_user = textarea_code.value
        #App over toolbar
        second_app = gui.Desktop(screen = Window,area = Frame)
        my_container2 = gui.Container(width =670,height = 500)
        second_app.connect(gui.QUIT,second_app.quit,None)
        second_app.connect(gui.QUIT,app.quit,None)
        #Exit button
        cancel_btn = gui.Button("Regresar")
        cancel_btn.connect(gui.CLICK,second_app.quit,None)
        cancel_btn.connect(gui.CLICK,app.quit,None)
        #Add items to container
        my_container2.add(gui.Image(const.imagespath+"Instrucciones_Background.png"),0,0)
        my_container2.add(cancel_btn,575,10)
        second_app.run(my_container2)
        pygame.display.flip()

    #Help button
    help_btn = gui.Button("Instrucciones")
    help_btn.connect(gui.CLICK, help)
    
    def file_treat():
        global Window,Frame
        #TODO Agregar imagen a botones y estilo a fondo
        third_app = gui.Desktop(screen = Window,area = Frame)
        third_app.connect(gui.QUIT,third_app.quit,None)
        third_app.connect(gui.QUIT,app.quit,None)
        my_container3 = gui.Container(width =670,height = 500)
        #Open button
        open_btn = gui.Button("Abrir")
        open_btn.connect(gui.CLICK,open_file_browser,True)
        #Save button
        save_btn = gui.Button("Guardar")
        save_btn.connect(gui.CLICK,open_file_browser,False)
        #Continue button / close file treatment
        ok_btn = gui.Button("Listo!")
        ok_btn.connect(gui.CLICK,third_app.quit,None)
        ok_btn.connect(gui.CLICK,app.quit,None)
        #Cancel button
        cancel_btn = gui.Button("Cancelar")
        cancel_btn.connect(gui.CLICK,third_app.quit,None)
        cancel_btn.connect(gui.CLICK,app.quit,None)

        #Add elements to container
        my_container3.add(gui.Image(const.imagespath+"Archivo_Background.png"),0,0)
        my_container3.add(open_btn,155,330)
        my_container3.add(save_btn,455,330)
        my_container3.add(ok_btn,310,375)
        my_container3.add(cancel_btn,580,10)
        third_app.run(my_container3)
        pygame.display.flip()
    
    #file treatment
    file_btn = gui.Button("Archivo")
    file_btn.connect(gui.CLICK,file_treat)

    # Display the background when playing as beginner
    def hint():
        global numero_hint, Window
        #Window.fill(const.green)
        if numero_hint < 5:
            numero_hint = numero_hint + 1
        else:
            numero_hint = 1
        #Hint images for level 1
        if dificulty_level == 1:
            if numero_hint == 1:
                img = image.load(const.imagespath+"Ayuda1_Background.png").convert_alpha()
            elif numero_hint == 2:
                img = image.load(const.imagespath+"Ayuda2_Background.png").convert_alpha()
            elif numero_hint == 3:
                img = image.load(const.imagespath+"Ayuda3_Background.png").convert_alpha()
            elif numero_hint == 4:
                img = image.load(const.imagespath+"Ayuda4_Background.png").convert_alpha()
            elif numero_hint == 5:
                img = image.load(const.imagespath+"Ayuda5_Background.png").convert_alpha()
            img.set_colorkey(RLEACCEL)
            rect = Rect((-8,35), (0, 0))
            #Window.fill(const.green)
            Window.blit(img, rect)
            #Update_display()
            pygame.display.flip()
    #Next tip button
    hint_btn = gui.Button("Siguiente tip")
    hint_btn.connect(gui.CLICK, hint)

    #Add items to container
    my_container1.add(Label_buttons, 462, 30)
    my_container1.add(cancel_btn,450,50)
    my_container1.add(save_btn,550,50)
    my_container1.add(file_btn,500,5)
    my_container1.add(Label_code, 419, 75)
    my_container1.add(textarea_code,419,95)
    my_container1.add(help_btn,480,470)
    if dificulty_level == 1:
        my_container1.add(hint_btn,145,415)
    app.run(my_container1) 

'''---------------------Pygame init--------------------'''
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

'''----------------Main loop starts----------------'''
while running:
    pygame.time.Clock().tick(10)
    for event in handle_widgets():
            if event.type == QUIT:
                quit()
                exit()
    if on_game:
        Window.fill(const.green)
        #Hint images for level 1
        if dificulty_level == 1:
            if numero_hint == 1:
                img = image.load(const.imagespath+"Ayuda1_Background.png").convert_alpha()
            elif numero_hint == 2:
                img = image.load(const.imagespath+"Ayuda2_Background.png").convert_alpha()
            elif numero_hint == 3:
                img = image.load(const.imagespath+"Ayuda3_Background.png").convert_alpha()
            elif numero_hint == 4:
                img = image.load(const.imagespath+"Ayuda4_Background.png").convert_alpha()
            elif numero_hint == 5:
                img = image.load(const.imagespath+"Ayuda5_Background.png").convert_alpha()
            img.set_colorkey(RLEACCEL)
            rect = Rect((-8,35), (0, 0))
            Window.blit(img, rect)
        keys = pygame.key.get_pressed()
        #Keyboard help finding solution
        if keys:
            if keys[K_h] and not executing:
                But_path()
                executing = True
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
        Label_gen.place((7, 30))
        #Widget for line counter
        entry_line_no = Entry(Frame,width=12,height=270,textcolor = Color("blue"),bold=True)
        entry_line_no.place((12,50))
        line_no = ""
        for value in range(1,50):
            line_no = line_no+str(value)+"\n\n"
        entry_line_no.set(line_no)
        #Visual of current code , non editable
        entryForInput = Entry(Frame,width=191,height=270)
        entryForInput.place((27,50))
        input_formatted = str(input_from_user)
        input_formatted = input_formatted.replace("\n","\n\n")
        entryForInput.set(input_formatted)
        #Score
        entry_score = Entry(Frame,width=90,height=10)
        entry_score.place((120,30))
        entry_score.set("Puntos:"+str(score))
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
        # Buttons
        # Levels section
        start_button= Button(Window, text = "Principiante", width = 95, height = 30, bordercolor = const.Porange, colour = const.yellow, fontsize = 18, target = Start_game)
        start_button.place((555, 25))
        expert_button= Button(Window, text = "Experto", width = 95, height = 30, bordercolor = const.white, colour = const.red, fontsize = 18, target = Expert_mode)
        expert_button.place((555, 64))
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
        # Bubble message text
        font = pygame.font.Font(None, 22)
        text = font.render("Bienvenid@ a", 1, Color(1,72,152))
        textpos = Rect((90,85),(125,195))
        Window.blit(text, textpos)
        text = font.render("Xilarius!!", 1, Color(1,72,152))
        textpos = Rect((120,125),(115,185))
        Window.blit(text, textpos)
        #Levels message
        font = pygame.font.Font(None, 22)
        text = font.render("Niveles", 1, (10,10,10))
        textpos = Rect((575,5),(50,45))
        Window.blit(text, textpos)
        render_widgets()
        pygame.display.flip()