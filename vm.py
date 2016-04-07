# -----------------------------------------------------------------------------
# Maquina Virtual: Xilarius
# Proyecto
# Ana Arellano   		A01089996
# Ana Karen Reyna		A01280310
# -----------------------------------------------------------------------------

from __future__ import print_function
from collections import deque
from semantica import Stack
from io import StringIO
from Class import *
import ast
import sys

#Mapeo de memoria
#1000 - 19999 <- Globales
#20000- 24999 <- Temporales
#25000- 25999 <- Constantes
global_mem_range = [1000,19999]
temp_mem_range = [20001,24999]
const_mem_range = [25000,25999]
xilarius = ''
class Machine:
    def __init__(self, globals,constants,temporary,cuadruplos):
        
        self.memory=globals
        self.constant =constants
        self.temporary = temporary
        self.instruction_pointer = 0
        self.code = cuadruplos
 #TODO Cambiar a usar estructura de cuadruplos
 #bajando el output del escaner  a un archivo
 #no input directo de codigo
    def run(self):
        while self.instruction_pointer < len(self.code):
            line = self.code[self.instruction_pointer]
            operators = line[1:]
            for value in operators:
                if value != '':
                    if (value >= temp_mem_range[0] and value <= temp_mem_range[1]) and not (value in self.memory):
                        self.memory[value]=self.temporary[value]  
                    elif (value >= const_mem_range[0] and value <= const_mem_range[1]) and not (value in self.memory):
                        self.memory[value]=self.constant[value]
            print(self.memory)
            self.dispatch(line)
            self.instruction_pointer+=1
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

    def exit(self):
        sys.exit(0)

    def minus(self,line):
        self.memory[line[3]] = int(self.memory[line[1]]) - int(self.memory[line[2]])
        print(self.memory[line[3]])
    def mul(self,line):
        self.memory[line[3]] = int(self.memory[line[1]]) * int(self.memory[line[2]])
        print(self.memory[line[3]])
    def div(self,line):
        self.memory[line[3]] = int( int(self.memory[line[1]]) / int(self.memory[line[2]]))
        print(self.memory[line[3]])
    def stop(self,line):
        print("parar")

    def eq(self,line):
        #self.memory[line[3]] =  int(self.memory[line[1]]) == self.memory[line[2]]
        return 0
    def noteq(self,line):
        #TODO Agregar conexion a interfaz
        return 0
#TODO Modificar a gotof
    def gotof(self,line):
        '''false_clause = self.pop()
        true_clause = self.pop()
        test = self.pop()
        self.push(true_clause if test else false_clause)
        '''
        return 0
    def goto(self,line):
        '''addr = self.pop()
        if isinstance(addr, int) and 0 <= addr < len(self.code):
            self.instruction_pointer = addr
        else:
            raise RuntimeError("JMP address must be a valid integer.")
        '''
        return 0
    def bwd(self,line):
        #TODO Conexion a interfaz para mover personaje
        global xilarius
        total = int(self.memory[line[1]])
        while(total > 0):
            xilarius.move(const.up)
        
    def fwd(self,line):
        #TODO Conexion a interfaz para mover personaje
        global xilarius
        total = int(self.memory[line[1]])
        while(total > 0):
            xilarius.move(const.down)
        
    def right(self,line):
        #TODO Conecion a interfaz para mover personaje
        global xilarius
        total = int(self.memory[line[1]])
        while(total > 0):
            xilarius.move(const.right)
        
    def left(self,line):
        #TODO Conecion a interfaz para mover personaje
        global xilarius
        total = int(self.memory[line[1]])
        while(total > 0):
            xilarius.move(const.left)
    def respond(self,line):
        #TODO Conecion a interfaz para mover personaje
        return 0
    def dump_stack(self):
        print("Data stack (top first):")

        for v in reversed(self.data_stack):
            print(" - type %s, value '%s'" % (type(v), v))

def runProgram():
    xilarius = character
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
if __name__ == "__main__":
    try:
        if len(sys.argv) > 1:
            cmd = sys.argv[1]
            if cmd == "test":
                runProgram()
            else:
                print("Commands: repl, test")
        
    except EOFError:
        print("")