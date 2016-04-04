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

class Machine:
    def __init__(self, code):
        self.data_stack = Stack()
        self.return_stack = Stack()
        self.instruction_pointer = 0
        self.code = code
#TODO Quitar esto por un acceso al objeto para la memoria virtual
    def pop(self):
        return self.data_stack.pop()

    def push(self, value):
        self.data_stack.push(value)

    def top(self):
        return self.data_stack.top()
 #TODO Cambiar a usar estructura de cuadruplos
 #bajando el output del escaner  a un archivo
 #no input directo de codigo
    def run(self):
        while self.instruction_pointer < len(self.code):
            opcode = self.code[self.instruction_pointer]
            self.instruction_pointer += 1
            self.dispatch(opcode)

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

        if op in dispatch_map:
            dispatch_map[op]()
        elif isinstance(op, int):
            self.push(op) # push numbers on stack
        elif isinstance(op, str) and op[0]==op[-1]=='"':
            self.push(op[1:-1]) # push quoted strings on stack
        else:
            raise RuntimeError("Unknown opcode: '%s'" % op)

    # OPERATIONS FOLLOW:
#TODO: Cambiar pila a valores de retorno para
#memoria virtual
    def plus(self):
        self.push(self.pop() + self.pop())

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

def test(code = [2, 3, "+", 5, "*", "println"]):


    print("Stack after running original program:")
    a = Machine(code)
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