# -----------------------------------------------------------------------------
# Escaner y Parser: Xilarius
# Proyecto
# Ana Arellano   		A01089996
# Ana Karen Reyna		A01280310
# -----------------------------------------------------------------------------

import sys
from semantica_variables import agregar_variable
sys.path.insert(0,"../..")

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
        '''program : MIPROGRAMA IDENTIFICADOR ENDLINE OPENEXP personaje modulo CLOSEEXP'''
        pass
#Specific error handling
def p_programa_error(p):
        '''program : MIPROGRAMA error ENDLINE OPENEXP personaje modulo CLOSEEXP'''
        print("Incorrect identifier " )
   
def p_personaje(p):
        '''personaje : CREARPERSONAJE IDENTIFICADOR ENDLINE vars'''
        pass
def p_modulo(p):
	'''modulo : moduloaux1 OPENCOND laberinto CLOSECOND OPENEXP instruccionaux CLOSEEXP instruccionaux
				| instruccion'''
	pass
def p_moduloaux1(p):
	'''moduloaux1 : SIES
			| REPETIRHASTA'''
	pass

def p_instruccion(p):
	'''instruccion : IDENTIFICADOR PUNTO instruccion1 ENDLINE instruccionaux'''
	pass
def p_instruccionaux(p):
	'''instruccionaux : 
                            | modulo'''
	pass

def p_instruccion1(p):
	'''instruccion1 : PARAR
			| mover OPENCOND expresion CLOSECOND
			| RESPONDER OPENCOND instruccion2 CLOSECOND'''
	pass
    
def p_instruccion2(p):
        '''instruccion2 : CTEESCRITA
                        | IDENTIFICADOR'''
        pass
def p_mover(p):
        '''mover : ATRAS
		| ADELANTE
		| DERECHA
		| IZQUIERDA'''
        pass
def p_vars(p):
        '''vars : 
                | vars2'''
        pass
#Specific error handling
def p_vars_error(p):
	'''vars : error IDENTIFICADOR tipo EQUALS varcte vars1'''
	print("Incorrect declaration " )
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
        '''vars2 : VAR IDENTIFICADOR tipo EQUALS varcte vars1
                | VAR IDENTIFICADOR tipo EQUALS CTEESCRITA vars1'''
        #Posible manera de incrustar la tabla de variables
        #TODO especificar en caso de error de semantica
        agregar_variable(p[2],p[5],p[3])
        pass
def p_laberinto(p):
	'''laberinto : laberinto1 laberinto2 varcte'''
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
def p_expresion(p):
	'''expresion : termino exp
                        | termino'''
	pass
#Specific error generation
def p_expresion_error(p):
        '''expresion : error exp
                        | termino error'''
        print("not a valid expresion" )  
def p_exp(p):
	'''exp : RESTA expresion
		| SUMA expresion'''
	pass
#Specific error generation
def p_exp_error(p):
        '''exp : error expresion'''
        print("not a valid operator" )  
        
def p_termino(p):
	'''termino : DIVISION varcte
                    | MULTIPLICACION varcte
                    | varcte'''
	pass
#Specific error generation
def p_termino_error(p):
        '''termino : error varcte'''
        print("not a valid operator" )
def p_tipo(p):
	'''tipo : TIPONUMERO
			| TIPOESCRITA
			| TIPODECISION'''
	pass
def p_varcte(p):
	'''varcte : IDENTIFICADOR
				| CTEENTERA
                                | CTEDECISION1
				| CTEDECISION2'''
	pass
	
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

    
