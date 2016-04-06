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
        
        self.memory={
             0:globals, #Globales {numeroenmemoria : (nombrereal, valor)}
             1:{}, #Temporales {numeroenmemoria : (nombrereal, valor)}
             2:{} #Constantes {numeroenmemoria :  valor}
            }
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
            self.dispatch(line)

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
            dispatch_map[op]()
        else:
            raise RuntimeError("Unknown opcode: '%s'" % op)

    # OPERATIONS FOLLOW:
#TODO: Cambiar pila a valores de retorno para
#memoria virtual
    def plus(self,line):
        print(line)

    def exit(self):
        sys.exit(0)

    def minus(self):
        last = self.pop()
        self.push(self.pop() - last)

    def mul(self):
        self.push(self.pop() * self.pop())

    def div(self):
        last = self.pop()
        self.push(self.pop() / last)

    def stop(self):
        b = self.pop()
        a = self.pop()
        self.push(b)
        self.push(a)

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

    temps = { 'temp4': 20005, 'temp9': 20010, 'temp8': 20009, 'temp6': 20007, 'temp2': 20003, 'temp3': 20004, 'temp5': 20006, 'temp1': 20002, 'temp0': 20000, 'temp7': 20008}
    glob = {'miPrograma': ('Primerprograma', {'Ana': ('personaje', 'personaje', 1003), 'Otravar': ('"hola"', 'escrita', 1000), 'Miotravar': ('3', 'numero', 1001), 'Mivar': ('verdadero', 'decision', 1002)})}
    const ={'pared': 25001, 'verdadero': 25000, '21': 25007, '1': 25006, '3': 25004, 'libre': 25002, '5': 25003, '4': 25005}
    code = {0: ['*', 25004, 25003, 20003], 1: ['*', 20003, 25005, 20004], 2: ['/', 20004, 1001, 20005], 3: ['-', 20005, 25006, 20006]}
    a = Machine(glob,const,temps,code)
    a.run()
    a.dump_stack()

    result = a.data_stack == b.data_stack
    print("Result: %s" % ("OK" if result else "FAIL"))
    return result

if __name__ == "__main__":
    try:
        if len(sys.argv) > 1:
            cmd = sys.argv[1]
            if cmd == "test":
                test()
            else:
                print("Commands: repl, test")
        else:
            repl()
    except EOFError:
        print("")