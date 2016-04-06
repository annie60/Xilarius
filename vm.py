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
import sys

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
 #TODO Cambiar a usar estructura de cuadruplos
 #bajando el output del escaner  a un archivo
 #no input directo de codigo
    def run(self):
        while self.instruction_pointer < len(self.code):
            line = self.code[self.instruction_pointer]
            operators = line[1:]
            for value in operators:
                if (value > temp_mem_range[0] and value < temp_mem_range[1]) and not (value in self.memory):
                    self.memory[value]=self.temporary[value]  
                elif (value > const_mem_range[0] and value < const_mem_range[1]) and not (value in self.memory):
                    self.memory[value]=self.constant[value]
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
            "atras":        self.bwd,
            "adelante":     self.fwd,
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
#TODO: Cambiar pila a valores de retorno para
#memoria virtual
    def plus(self,line):
        self.memory[line[3]] = int(self.memory[line[1]]) + int(self.memory[line[2]])
        

    def exit(self):
        sys.exit(0)

    def minus(self,line):
        self.memory[line[3]] = int(self.memory[line[1]]) - int(self.memory[line[2]])
        
    def mul(self,line):
        self.memory[line[3]] = int(self.memory[line[1]]) * int(self.memory[line[2]])
        
    def div(self,line):
        self.memory[line[3]] = int( int(self.memory[line[1]]) / int(self.memory[line[2]]))
        
    def stop(self):
        print()

    def eq(self):
        #TODO Agregar conexion a interfaz 
        # isWall? == verdadero
        self.push(self.pop() == self.pop())
    
    def noteq(self):
        #TODO Agregar conexion a interfaz
        self.push(self.pop() != self.pop())
        
#TODO Modificar a gotof
    def gotof(self):
        false_clause = self.pop()
        true_clause = self.pop()
        test = self.pop()
        self.push(true_clause if test else false_clause)

    def goto(self):
        addr = self.pop()
        if isinstance(addr, int) and 0 <= addr < len(self.code):
            self.instruction_pointer = addr
        else:
            raise RuntimeError("JMP address must be a valid integer.")
    def bwd(self):
        #TODO Conexion a interfaz para mover personaje
        return 0
    def fwd(self):
        #TODO Conexion a interfaz para mover personaje
        return 0
    def right(self):
        #TODO Conecion a interfaz para mover personaje
        return 0
    def left(self):
        #TODO Conecion a interfaz para mover personaje
        return 0
    def respond(self):
        #TODO Conecion a interfaz para mover personaje
        return 0
    def dump_stack(self):
        print("Data stack (top first):")

        for v in reversed(self.data_stack):
            print(" - type %s, value '%s'" % (type(v), v))

def test():
#TODO: Cambiar a que lea de archivo
    temps = {20003:'temp2',20004:'temp3'}
    glob = {1003:'personaje' , 1000:'2'}
    const ={ 25004:'3' ,  25003:'5'}
    code = {0: ['+',25004,25003,20003], 1: ['-',20003,1000,20004]}
    #code = {0: ['*', 25004, 25003, 20003], 1: ['*', 20003, 25005, 20004], 2: ['/', 20004, 1001, 20005], 3: ['-', 20005, 25006, 20006]}
    a = Machine(glob,const,temps,code)
    a.run()
    print(a.memory)
if __name__ == "__main__":
    try:
        if len(sys.argv) > 1:
            cmd = sys.argv[1]
            if cmd == "test":
                test()
            else:
                print("Commands: repl, test")
        
    except EOFError:
        print("")