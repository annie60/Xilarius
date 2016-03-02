# -----------------------------------------------------------------------------
# Escaner y Parser: Xilarius
# Proyecto
# Ana Arellano   		A01089996
# Ana Karen Reyna		A01280310
# -----------------------------------------------------------------------------

import sys
sys.path.insert(0,"../..")

if sys.version_info[0] >= 3:
    raw_input = input
#Token ids
tokens = (
    'MIPROGRAMA','IDENTIFICADOR','ENDLINE',
	'OPENEXP','CLOSEEXP','CREARPERSONAJE','SIES',
	'OPENCOND','CLOSECOND','REPETIRHASTA',
    'PUNTO','PARAR','RESPONDER','CTEDECISION1','CTEDECISION2','ATRAS',
    'ADELANTE','DERECHA','IZQUIERDA','VAR','EQUALS','COMA',
    'PARED','LIBRE','META','IGUALA','DIFERENTEA',
    'SUMA','RESTA','DIVISION','MULTIPLICACION',
	'CTEENTERA','TIPONUMERO','TIPOESCRITA','TIPODECISION'
    )

# Tokens
t_MIPROGRAMA = r'miPrograma'
t_IDENTIFICADOR = r'[a-zA-Z][_a-zA-Z0-9]*'
t_ENDLINE = r';'
t_OPENEXP = r'{'
t_CLOSEEXP = r'}'
t_CREARPERSONAJE = r'crearPersonaje'
t_SIES = r'siEs'
t_OPENCOND = r'\('
t_CLOSECOND = r'\)'
t_REPETIRHASTA = r'repetirHasta'
t_PUNTO = r'.'
t_PARAR = r'parar'
t_RESPONDER = r'responder'
r_CTEDECISION1 = r'verdadero'
r_CTEDECISION2 = r'falso'

t_ATRAS = r'atras'
t_ADELANTE = r'adelante'
t_DERECHA = r'derecha'
t_IZQUIERDA = r'izquierda'
t_VAR = r'var'
t_EQUALS = r'='
t_COMA = r','
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


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
    
# Build the lexer
import ply.lex as lex
lex.lex()


# Parsing rules

def p_programa(p):
    '''program : MIPROGRAMA IDENTIFICADOR ENDLINE OPENEXP personaje modulo CLOSEEXP'''
    pass
def p_personaje(p):
    '''personaje : CREARPERSONAJE IDENTIFICADOR ENDLINE vars
                | CREARPERSONAJE IDENTIFICADOR ENDLINE'''
    pass
# DUDAS
def p_modulo(p):
	'''modulo : moduloaux1 OPENCOND laberinto CLOSECOND OPENEXP modulo moduloaux2
				| instruccion'''
	pass
def p_moduloaux1(p):
	'''moduloaux1 : SIES
					| REPETIRHASTA'''
	pass
def p_moduloaux2(p):
	'''moduloaux2 : modulo CLOSEEXP modulo
					| CLOSEEXP modulo
					| CLOSEEXP'''
	pass
	
	
def p_instruccion(p):
	'''instruccion : IDENTIFICADOR PUNTO instruccion1 instruccion2'''
	pass

def p_instruccion1(p):
	'''instruccion1 : PARAR
					| mover OPENCOND expresion CLOSECOND
					| RESPONDER OPENCOND instruccion3 CLOSECOND'''
	pass

def p_instruccion2(p):
	'''instruccion2 : ENDLINE instruccion
					| ENDLINE'''
	pass

def p_instruccion3(p):
	'''instruccion3 : IDENTIFICADOR
					| CTEDECISION1
					| CTEDECISION2'''
	pass

def p_mover(p):
	'''mover : ATRAS
				| ADELANTE
				| DERECHA
				| IZQUIERDA'''
	pass

def p_vars(p):
	'''vars : VAR IDENTIFICADOR tipo EQUALS vars1 vars2'''
	pass
def p_vars1(p):
	'''vars1 : varcte
				| varcte2'''
	pass

def p_vars2(p):
	'''vars2 : COMA vars
				| ENDLINE'''
	pass
	
def p_laberinto(p):
	'''laberinto : laberinto1 laberinto2 laberinto3'''
	pass
def p_laberinto1(p):
	'''laberinto1 : PARED
					| LIBRE
					| META'''
	pass
def p_laberinto2(p):
	'''laberinto2 : DIFERENTEA
					| IGUALA'''
	pass
def p_laberinto3(p):
	'''laberinto3 : IDENTIFICADOR
					| CTEDECISION1
					| CTEDECISION2'''
	pass
def p_expresion(p):
	'''expresion : termino SUMA
					| termino RESTA
					| termino'''
	pass
def p_termino(p):
	'''termino : varcte DIVISION
				| varcte MULTIPLICACION
				| varcte'''
	pass
def p_tipo(p):
	'''tipo : TIPONUMERO
			| TIPOESCRITA
			| TIPODECISION'''
	pass
def p_varcte(p):
	'''varcte : IDENTIFICADOR
				| CTEENTERA'''
	pass
def p_varcte2(p):
	'''varcte2 : CTEENTERA
				| CTEDECISION1
				| CTEDECISION2'''
	pass
	
	

def p_error(p):
    if p:
        print("Syntax error at '%s'" % p.value)
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

    
