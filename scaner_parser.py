# -----------------------------------------------------------------------------
# Escaner y Parser: Xilarius
# Proyecto
# Ana Arellano   		A01089996
# Ana Karen Reyna		A01280310
# -----------------------------------------------------------------------------

import sys
from semantica import agregar_variable,operacion_compatible,cuadruplo,crear_modulo,operacion
from semantica import Stack
from semantica import Queue
sys.path.insert(0,"../..")
#Inicializacion de objetos auxiliares
ids = Queue()
types = Stack()
operations = Stack()
values = Stack()
pOper = Stack()
pilaO =Stack()
if sys.version_info[0] >= 3:
    raw_input = input
#Token ids
tokens = (
    'MIPROGRAMA','IDENTIFICADOR','ENDLINE',
	'OPENEXP','CLOSEEXP','CREARPERSONAJE','SIES',
	'OPENCOND','CLOSECOND','REPETIRHASTA',
    'PUNTO','PARAR','RESPONDER','CTEDECISION1','CTEDECISION2','CTEESCRITA','ATRAS',
    'ADELANTE','DERECHA','IZQUIERDA','VAR','EQUALS','COMA',
    'PARED','LIBRE','META','IGUALA','DIFERENTEA',
    'SUMA','RESTA','DIVISION','MULTIPLICACION',
	'CTEENTERA','TIPONUMERO','TIPOESCRITA','TIPODECISION'
    )

# Tokens
t_MIPROGRAMA = r'miPrograma'
t_IDENTIFICADOR = r'[A-Z][_a-zA-Z0-9]*'
t_ENDLINE = r';'
t_OPENEXP = r'{'
t_CLOSEEXP = r'}'
t_CREARPERSONAJE = r'crearPersonaje'
t_SIES = r'siEs'
t_OPENCOND = r'\('
t_CLOSECOND = r'\)'
t_REPETIRHASTA = r'repetirHasta'
t_PUNTO = r'\.'
t_PARAR = r'parar'
t_RESPONDER = r'responder'
t_CTEDECISION1 = r'verdadero'
t_CTEDECISION2 = r'falso'
t_CTEESCRITA = r'\"[a-zA-Z0-9 \?\']*\"'
t_ATRAS = r'atras'
t_ADELANTE = r'adelante'
t_DERECHA = r'derecha'
t_IZQUIERDA = r'izquierda'
t_VAR = r'var'
t_EQUALS = r'='
t_COMA = r'\,'
t_PARED = r'pared'
t_LIBRE = r'libre'
t_META = r'meta'
t_IGUALA = r'=='
t_DIFERENTEA = r'<>'
t_SUMA = r'\+'
t_RESTA = r'-'
t_DIVISION = r'/'
t_MULTIPLICACION = r'\*'
t_CTEENTERA = r'[0-9][0-9]*'
t_TIPONUMERO = r'numero'
t_TIPOESCRITA = r'escrita'
t_TIPODECISION = r'decision'

t_ignore = " \t"

# Error handling
def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
    
# Build the lexer
import ply.lex as lex
lex.lex()
#Debbuging instruction
#lex.runmain()

# Parsing rules

def p_programa(p):
    '''program : declarar ENDLINE OPENEXP personaje modulo CLOSEEXP'''
    pass
    
def p_declarar(p):
    '''declarar : MIPROGRAMA IDENTIFICADOR'''
    ids.enqueue(p[2])
    types.push(p[1])
    if ids.size() >= 1:
        tipo = types.pop()
        identificador =ids.dequeue()
        crear_modulo(identificador,tipo)
#Specific error handling
def p_programa_error(p):
        '''program : MIPROGRAMA error ENDLINE OPENEXP personaje modulo CLOSEEXP'''
        print("Incorrect identifier " )
   
def p_personaje(p):
    '''personaje : CREARPERSONAJE IDENTIFICADOR ENDLINE vars'''
    pass
    ids.enqueue(p[2])
    types.push("personaje")
    values.push("personaje")
    if ids.size() >= 1:
        tipo = types.pop()
        valor = values.pop()
        identificador =ids.dequeue()
        agregar_variable(identificador,valor,tipo)
def p_modulo(p):
    '''modulo : moduloaux1 OPENCOND laberinto CLOSECOND OPENEXP instruccionaux CLOSEEXP instruccionaux
				| instruccion'''
    pass
def p_moduloaux1(p):
	'''moduloaux1 : SIES
			| REPETIRHASTA'''
	pass
        
def p_instruccion(p):
    '''instruccion : instruccion5 instruccionaux'''
    pass
    
def p_instruccion5(p):
    '''instruccion5 : IDENTIFICADOR PUNTO instruccion1 ENDLINE'''
    types.push(p[1])
    pOper.push(p[1])
    if values.size() >= 1:
        valor = values.pop()
        operation = operations.pop()
        tipo = types.pop()
        operder =pOper.pop()
        operizq = pOper.pop()
        operador = pilaO.pop()
        operacion(operation,valor,tipo)
        print("Instruccion "+operador+" "+str(operder)+" "+str(operizq))
def p_instruccionaux(p):
	'''instruccionaux : 
                            | modulo'''
	pass

def p_instruccion1(p):
    '''instruccion1 : instruccion4
			| mover OPENCOND expresion CLOSECOND
			| instruccion3'''
    pass

def p_instruccion4(p):
    '''instruccion4 : PARAR'''
    pass
    operations.push(p[1])
    values.push("personaje")
    pilaO.push(p[1])
    pOper.push(p[1])
def p_instruccion3(p):
    '''instruccion3 : RESPONDER OPENCOND instruccion2 CLOSECOND'''
    pass 
    operations.push(p[1])
    pilaO.push(p[1])
def p_instruccion2(p):
    '''instruccion2 : CTEESCRITA
                        | IDENTIFICADOR'''
    pass
    values.push(p[1])
    pOper.push(p[1])
def p_mover(p):
    '''mover : ATRAS
		| ADELANTE
		| DERECHA
		| IZQUIERDA'''
    pass
    operations.push(p[1])
    pilaO.push(p[1])
def p_vars(p):
        '''vars : 
                | vars2'''
        pass
#Specific error handling
def p_vars_error(p):
    '''vars : error IDENTIFICADOR tipo EQUALS varcte vars1'''
    line = p.lineno(1)
    print("Incorrect declaration near line "+line )
#Specific error handling
def p_vars_error2(p):
	'''vars : CREARPERSONAJE error'''
	print("More than one character declare" )
        
def p_vars1(p):
    '''vars1 : COMA vars2
        	| ENDLINE'''
    pass  
#Specific error handling
def p_vars2_error(p):
	'''vars1 : COMA error ENDLINE'''
	print("Extra ',' " )
def p_vars2(p):
        '''vars2 : VAR IDENTIFICADOR tipo EQUALS varcte vars1'''
        pass
        ids.enqueue(p[2])
        if ids.size() >= 1:
            valor = values.pop()
            tipo = types.pop()
            identificador =ids.dequeue()
            pOper.pop()
            agregar_variable(identificador,valor,tipo)
def p_laberinto(p):
    '''laberinto : laberinto1 laberinto2 varcte'''
    pass
    if values.size() >= 1:
        valor = values.pop()
        tipo = types.pop()
        operacion = operations.pop()
        ##TODO: Specify use of thi evalution
        pOper.pop()
        operacion_compatible(operacion,tipo,valor)
def p_laberinto1(p):
    '''laberinto1 : PARED
		| LIBRE
		| META'''
    pass
    types.push("decision")
def p_laberinto2(p):
    '''laberinto2 : DIFERENTEA
	| IGUALA'''
    pass
    operations.push(p[1])
def p_expresion(p):
    '''expresion : termino exp'''
    pass 
#Specific error generation
def p_expresion_error(p):
        '''expresion : error exp
                        | termino error'''
        print("not a valid expresion" )  
def p_exp(p):
    '''exp :
            | exp2 exp'''
    pass

def p_exp2(p):
    '''exp2 : RESTA termino 
            | SUMA termino'''
    pass
    pilaO.push(p[1])
    if pilaO.top() == "+" or pilaO.top() == "-":
        operador = pilaO.pop()
        operDer = pOper.pop()
        operIzq = pOper.pop()
        temporal = cuadruplo(operador,operIzq,operDer)
        print(str(operIzq)+operador+str(operDer)+"="+str(temporal)+" +/-")
        pOper.push(temporal)
#Specific error generation
def p_exp_error(p):
        '''exp2 : error termino '''
        print("not a valid operator" )   
def p_termino(p):
    '''termino : varcte termino2'''
    pass
def p_termino2(p):
    '''termino2 : 
                | termino3 termino2'''
    pass
    
def p_termino3(p):
    '''termino3 : DIVISION varcte
                | MULTIPLICACION varcte'''
    pass
    pilaO.push(p[1])
    if pilaO.top() == "*" or pilaO.top() == "/":
        operador = pilaO.pop()
        operDer = pOper.pop()
        operIzq = pOper.pop()
        temporal = cuadruplo(operador,operIzq,operDer)
        print(str(operIzq)+operador+str(operDer)+"="+str(temporal)+" * /")
        pOper.push(temporal)
def p_tipo(p):
    '''tipo : TIPONUMERO
		| TIPOESCRITA
		| TIPODECISION'''
    pass  
    types.push(p[1])
    
def p_varcte(p):
    '''varcte : IDENTIFICADOR
        	| CTEENTERA
                | CTEDECISION1
		| CTEDECISION2
                | CTEESCRITA'''
    pass
    values.push(p[1])
    pOper.push(p[1])
#Error handling
def p_error(p):
    if p:
        print("Syntax error near '%s'" % p.value)
        print("On line ",p.lineno)
        
    else:
        print("Syntax error at EOF")

import ply.yacc as yacc
yacc.yacc()


import sys
try:
    f = open(sys.argv[1])
    p = yacc.parse(f.read())
    print(p)
except EOFError:
    print("Could not open file %s." % sys.argv[1])

    
