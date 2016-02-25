# -----------------------------------------------------------------------------
# Escaner y Parser: lenguaje patito
# Tarea 3
# A01089996
# -----------------------------------------------------------------------------

import sys
sys.path.insert(0,"../..")

if sys.version_info[0] >= 3:
    raw_input = input
#Token ids
tokens = (
    'PROGRAM','IDENTIFIER','ASSIGN','EQUALS',
    'ENDLINE','OPENCOND','CLOSECOND','OPENEXP',
    'CLOSEEXP','SEPARATE',
    'LESSTHAN','MORETHAN','DIFFERENT','PLUS','MINUS',
    'TIMES','DIVIDE','IF','ELSE','PRINT','TYPEINT',
    'TYPEFLOAT','VARIABLE',
    'INTEGER','FLOATNUM','STRING'
    )

# Tokens
t_ASSIGN = r':'
t_EQUALS =r'='
t_ENDLINE =r';'
t_OPENCOND = r'\('
t_CLOSECOND =r'\)'
t_OPENEXP =r'{'
t_CLOSEEXP =r'}'
t_SEPARATE = r','
t_LESSTHAN=r'<'
t_MORETHAN=r'>'
t_DIFFERENT=r'<>'
t_PLUS=r'\+'
t_MINUS=r'-'
t_TIMES=r'\*'
t_DIVIDE= r'/'
t_TYPEINT= r'int'
t_TYPEFLOAT=r'float'
t_IF =r'if'
t_ELSE =r'else'
t_PRINT = r'print'
t_VARIABLE =r'var'
t_PROGRAM = r'program'
t_IDENTIFIER=r'[_][a-zA-Z0-9]*'
t_STRING    = r'[A-Z][a-zA-Z]*'
t_INTEGER = r'[0-9][0-9]*'
t_FLOATNUM =r'[0-9][0-9]*\.?[0-9][0-9]*'

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

def p_program(p):
    '''program : PROGRAM IDENTIFIER ENDLINE program1'''
    pass
def p_program1(p):
    '''program1 : vars program2 
                | program2'''
    pass
def p_program2(p):
    '''program2 : block'''
    pass
def p_vars(p):
    "vars : VARIABLE vars1"
    pass
def p_vars1(p):
    "vars1 : IDENTIFIER vars2"
    pass
def p_vars1_error(p):
    "vars1 : error vars2"
    print("Missing identifier for variable")
def p_vars2(p):
    '''vars2 : vars3 
            | SEPARATE vars1 '''
    pass
def p_vars3(p):
    '''vars3 : ASSIGN TYPEINT ENDLINE 
            | ASSIGN TYPEFLOAT ENDLINE 
            | ASSIGN TYPEINT ENDLINE vars1 
            | ASSIGN TYPEFLOAT ENDLINE vars1 '''
    pass
#Version with error detection
def p_vars3_error(p):
    '''vars3 : ASSIGN TYPEINT error 
            | ASSIGN TYPEFLOAT error 
            | ASSIGN TYPEINT error vars1 
            | ASSIGN TYPEFLOAT error vars1 '''
    print("Missing ';' ")
def p_block(p):
    "block : OPENEXP block1"
    pass
def p_block1(p):
    '''block1 : estat block1 
                | CLOSEEXP'''
    pass
def p_estat(p):
    '''estat : asignation 
               | condition 
               | writing'''
    pass
def p_asignation(p):
    "asignation : IDENTIFIER EQUALS expression ENDLINE"
    pass
def p_condition(p):
    '''condition : IF OPENCOND expression CLOSECOND block condition1 ENDLINE'''
    pass
def p_condition_error(p):
    '''condition : IF error expression CLOSECOND block condition1 ENDLINE'''
    print ("Missing '(' in condition ")

def p_condition1(p):
    '''condition1 : empty
                    | ELSE block'''
    pass
def p_writing(p):
    "writing : PRINT OPENCOND writing1 CLOSECOND ENDLINE"
    pass
def p_writing1(p):
    '''writing1 : expression 
                | expression SEPARATE writing1 
                | STRING'''
    pass
def p_writing_error(p):
    "writing : PRINT OPENCOND writing1 CLOSECOND error"
    print("Missing ';'")
def p_expression(p):
    ''' expression : exp LESSTHAN exp 
                    | exp MORETHAN exp 
                    | exp DIFFERENT exp
                    | exp'''
    pass
def p_empty(p):
    "empty :"
    pass
def p_exp(p):
    '''exp : term exp1 
            | term'''
    pass
def p_exp1(p):
    '''exp1 : MINUS exp 
            | PLUS exp'''
    pass
def p_exp1_error(p):
    '''exp1 : error exp'''
    print("not a valid operator" )
def p_term(p):
    '''term : factor term1 
            | factor'''
    pass
def p_term1(p):
    '''term1 : TIMES term 
            | DIVIDE term'''
def p_factor(p):
    '''factor : OPENCOND expression CLOSECOND 
                | factor1 
                | MINUS factor1 
                | PLUS factor1'''
def p_factor1(p):
    "factor1 : constant"
def p_constant(p):
    '''constant : IDENTIFIER 
                | INTEGER
                | FLOATNUM'''

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

    
