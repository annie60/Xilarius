# -----------------------------------------------------------------------------
# Escaner y Parser: Xilarius
# Proyecto
# Ana Arellano   		A01089996
# Ana Karen Reyna		A01280310
# -----------------------------------------------------------------------------

import sys
from semantica import obtener_direccion,agregar_variable,operacion_compatible,crear_modulo,operacion, asignar_valor_variable
from semantica import Stack,crear_archivo_salida
from semantica import Queue
sys.path.insert(0,"../..")
#Helpers initialization
ids = Queue()
types = Stack()
operations = Stack()
values = Stack()
pOper = Stack()
pilaO =Stack()
braces = Stack()
pSaltos = Stack()
negative = Stack()
cuadruplos = {}
build_errors=[]
#Helper counters
temp_counter = 0
counter = 0
if sys.version_info[0] >= 3:
    raw_input = input
#Token ids
tokens = (
    'MIPROGRAMA','IDENTIFICADOR','ENDLINE',
	'OPENEXP','CLOSEEXP','CREARPERSONAJE','SIES',
	'OPENCOND','CLOSECOND','REPETIRMIENTRAS',
    'PUNTO','PARAR','RESPONDER','CTEDECISION1','CTEDECISION2','CTEESCRITA','ARRIBA',
    'ABAJO','DERECHA','IZQUIERDA','VAR','EQUALS','COMA',
    'PAREDDERECHA','PAREDIZQUIERDA','PAREDARRIBA','PAREDABAJO','LIBREDERECHA','LIBREIZQUIERDA','LIBREARRIBA','LIBREABAJO','METADERECHA','METAIZQUIERDA','METAARRIBA','METAABAJO','IGUALA','DIFERENTEA',
    'SUMA','RESTA','DIVISION','MULTIPLICACION',
	'CTEENTERA','TIPONUMERO','TIPOESCRITA','TIPODECISION','NOT','HACERESCRITA','O'
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
t_REPETIRMIENTRAS = r'repetirMientras'
t_PUNTO = r'\.'
t_PARAR = r'parar'
t_RESPONDER = r'responder'
t_CTEDECISION1 = r'verdadero'
t_CTEDECISION2 = r'falso'
t_CTEESCRITA = r'\"[a-zA-Z0-9 \?\']*\"'
t_ARRIBA = r'arriba'
t_ABAJO = r'abajo'
t_DERECHA = r'derecha'
t_IZQUIERDA = r'izquierda'
t_VAR = r'var'
t_EQUALS = r'='
t_COMA = r'\,'
t_PAREDDERECHA = r'paredDerecha'
t_PAREDIZQUIERDA = r'paredIzquierda'
t_PAREDARRIBA = r'paredArriba'
t_PAREDABAJO = r'paredAbajo'
t_LIBREDERECHA = r'libreDerecha'
t_LIBREIZQUIERDA = r'libreIzquierda'
t_LIBREARRIBA = r'libreArriba'
t_LIBREABAJO = r'libreAbajo'
t_METADERECHA = r'metaDerecha'
t_METAIZQUIERDA = r'metaIzquierda'
t_METAARRIBA = r'metaArriba'
t_METAABAJO = r'metaAbajo'
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
t_NOT = r'no'
t_HACERESCRITA = r'hacerEscrita'
t_O = r'o'
t_ignore = " \t"

# Error handling
def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")                 
def t_error(t):
    global build_errors
    build_errors.append("Caracter ilegal: '%s'" % t.value[0])
    t.lexer.skip(1)
    


# Parsing rules
#----------------------------------------------
def p_programa(p):
    '''program : declarar ENDLINE program2 personaje modulo CLOSEEXP'''
    pass
    if not braces.isEmpty():
        braces.pop()
    #At the end sends the information to an output file
    crear_archivo_salida(cuadruplos)

def p_program2(p):
    '''program2 : OPENEXP'''
    braces.push(p[1])
def p_program2_error(p):
    '''program2 : error'''
    pass
    global build_errors
    build_errors.append("Error: Falta '{'")
def p_declarar(p):
    '''declarar : MIPROGRAMA IDENTIFICADOR'''
    ids.enqueue(p[2])
    types.push(p[1])
    if ids.size() >= 1:
        tipo = types.pop()
        identificador =ids.dequeue()
        #Creates main structure of function dictionary
        #For further semantics validation
        crear_modulo(identificador,tipo)
##Character declaration
##-----------------------------------
def p_personaje(p):
    '''personaje : CREARPERSONAJE IDENTIFICADOR ENDLINE vars'''
    pass
##Glob. var. declaration
    ids.enqueue(p[2])
    types.push("personaje")
    values.push("personaje")
    global build_errors
    if ids.size() >= 1:
        tipo = types.pop()
        valor = values.pop()
        identificador =ids.dequeue()
        #Checks for semantic mistakes
        respuesta_semantica =agregar_variable(identificador,valor,tipo)
        if (respuesta_semantica != ""):
            build_errors.append(respuesta_semantica)
#Specific error handling
def p_personaje_error(p):
    '''personaje : CREARPERSONAJE error ENDLINE vars'''
    global build_errors
    build_errors.append("Error: No se encontro nombre de personaje")
def p_personaje_error2(p):
    '''personaje : error'''
    global build_errors
    build_errors.append("Error: No se encontro personaje")
##Start of the modules for flow control
##-----------------------------------
def p_modulo(p):
    '''modulo : moduloaux1 
		| moduloaux2
                | instruccion'''
    pass
    ##Braces equality check
    if not braces.isEmpty():
        braces.pop()
def p_moduloaux1(p):
    '''moduloaux1 : SIES OPENCOND laberinto CLOSECOND modulo2 instruccionaux modulo3 instruccionaux'''
    pass
##Loops and decitions control
def p_modulo3(p):
    '''modulo3 : CLOSEEXP modulo6'''
    pass
    if not pSaltos.isEmpty():
        global counter
        cuadruplos[pSaltos.pop()][3]=counter   
def p_modulo4(p):
    '''modulo4 : CLOSEEXP'''
    pass
    if not pSaltos.isEmpty():
        global counter
        cuadruplos[pSaltos.pop()][3]=counter+1
        #Loops operation creation for vm
        #So it can jump back to check condition
        if not pSaltos.isEmpty():
            cuadruplos[counter]=["goto","","",pSaltos.pop()]
            counter+=1
def p_moduloaux2(p):
    '''moduloaux2 : moduloaux3 OPENCOND laberinto CLOSECOND modulo2 instruccionaux modulo4 instruccionaux'''
    pass
## While rules
def p_moduloaux3(p):
    '''moduloaux3 : REPETIRMIENTRAS'''
    pass
    #For loops control
    pSaltos.push(counter)
def p_modulo2(p):
    '''modulo2 : OPENEXP'''
    pass
    #Part of parenthesis equality control
    braces.push(p[1])
def p_modulo2_error(p):
    '''modulo2 : error'''
    global build_errors
    build_errors.append("Error: Falta '{'")
##If else rules
def p_modulo5(p):
    '''modulo5 : O '''
    pass
    global counter
    #Removes current gotof
    falso = pSaltos.pop()
    #Fills with current pointer plus one
    cuadruplos[falso][3] = counter+1
    #Inserts current pointer to attend later
    pSaltos.push(counter)
    #Creates jump quadruple
    cuadruplos[counter]=["goto","","",""]
    counter+=1
def p_modulo6(p):
    '''modulo6 : modulo5 moduloaux1
                | '''
    pass
##Character instructions start
## -------------------------
def p_instruccion(p):
    '''instruccion : instruccion5 instruccionaux'''
    pass
    #Equality control for braces
    braces.push('{')
def p_instruccion5(p):
    '''instruccion5 : IDENTIFICADOR instruccion6 ENDLINE'''
    types.push(p[1])
    pOper.push(p[1])
    if values.size() >= 1:
        global counter,temp_counter
        valor = values.pop()
        tipo = types.pop()
        operder =pOper.pop()
        operizq = pOper.pop()
        operador = pilaO.pop()
        if operations.isEmpty():
            respuesta_semantica = operacion_compatible(operador,valor,tipo)
        else:
            operation = operations.pop()
            respuesta_semantica = operacion(operation,valor,tipo)
        global build_errors
        if respuesta_semantica == "":
            dir_der=obtener_direccion(operder)
            dir_izq=obtener_direccion(operizq)
        else:
            dir_der=obtener_direccion(operder)
            dir_izq=obtener_direccion(operizq)
            build_errors.append(respuesta_semantica)
        
        pOper.push("temp"+str(temp_counter))
        cuadruplos[counter] = [operador,dir_izq,dir_der,""]
        counter+=1
def p_instruccion6(p):
    '''instruccion6 : PUNTO instruccion1
                    | asignarvalor'''
##Error control for sintaxis        
def p_instruccion5_error(p):
    '''instruccion5 : IDENTIFICADOR instruccion6 error'''
    global build_errors
    build_errors.append("Error: Falta ';'")
    types.push(p[1])
    pOper.push(p[1])
    if values.size() >= 1:
        global counter,temp_counter
        #For compatibility oepration
        valor = values.pop()
        tipo = types.pop()
        #For quadruples
        operder =pOper.pop()
        operizq = pOper.pop()
        operador = pilaO.pop()
        if operations.isEmpty():
            respuesta_semantica = operacion_compatible(operador,valor,tipo)
        else:
            operation = operations.pop()
            respuesta_semantica = operacion(operation,valor,tipo)
        #Get logical directions for vm
        if respuesta_semantica == "":
            dir_der=obtener_direccion(operder)
            dir_izq=obtener_direccion(operizq)
        else:
            dir_der=obtener_direccion(operder)
            dir_izq=obtener_direccion(operizq)
            build_errors.append(respuesta_semantica)
        #Insert result to stack
        pOper.push("temp"+str(temp_counter))
        cuadruplos[counter] = [operador,dir_izq,dir_der,""]
        counter+=1
#Specific error generation
def p_instruccion5_error2(p):
    '''instruccion5 : IDENTIFICADOR error ENDLINE'''
    global build_errors
    build_errors.append("Error: Falta '.' o '='")
    types.push(p[1])
    pOper.push(p[1])
    if values.size() >= 1:
        global counter,temp_counter
        valor = values.pop()
        tipo = types.pop()
        operder =pOper.pop()
        operizq = pOper.pop()
        operador = pilaO.pop()
        if operations.isEmpty():
            respuesta_semantica = operacion_compatible(operador,valor,tipo)
        else:
            operation = operations.pop()
            respuesta_semantica = operacion(operation,valor,tipo)
        if respuesta_semantica == "":
            dir_der=obtener_direccion(operder)
            dir_izq=obtener_direccion(operizq)
        else:
            dir_der=obtener_direccion(operder)
            dir_izq=obtener_direccion(operizq)
            build_errors.append(respuesta_semantica)
        
        pOper.push("temp"+str(temp_counter))
        cuadruplos[counter] = [operador,dir_izq,dir_der,""]
        counter+=1
##Auxiliar instruction rules
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
    pOper.push("")
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
    '''mover : ARRIBA
		| ABAJO
		| DERECHA
		| IZQUIERDA'''
    pass
    operations.push(p[1])
    pilaO.push(p[1])
##Global vars. definition rules
##-------------------------------------------
def p_vars(p):
        '''vars : 
                | vars2'''
        pass
#Specific error handling
def p_vars_error(p):
    '''vars : error IDENTIFICADOR tipo EQUALS varcte vars1'''
    global build_errors
    build_errors.append("Error: Declaracion incorrecta")
#Specific error handling
def p_vars_error2(p):
    '''vars : CREARPERSONAJE error'''
    build_errors.append("Error: Mas de un personaje declarado")
def p_vars1(p):
    '''vars1 : COMA vars2
        	| ENDLINE'''
    pass  
#Specific error handling
def p_vars2_error(p):
    '''vars1 : COMA error ENDLINE'''
    global build_errors
    build_errors.append("Error: Extra ','")
def p_vars2(p):
        '''vars2 : VAR IDENTIFICADOR tipo EQUALS varcte vars1'''
        pass
        global build_errors
        ids.enqueue(p[2])
        if ids.size() >= 1:
            valor = values.pop()
            tipo = types.pop()
            identificador =ids.dequeue()
            pOper.pop()
            respuesta_semantica =agregar_variable(identificador,valor,tipo)
            if (respuesta_semantica != ""):
                build_errors.append(respuesta_semantica)
#Asign values
#------------------------------------------
def p_asignarvalor(p):
        '''asignarvalor : EQUALS valores'''
        pass
        pilaO.push(p[1])
def p_valores(p):
        '''valores : expresion
                    | convierte'''
        pass
#Types change
#----------------------------------------
def p_convierte(p):
    '''convierte : HACERESCRITA OPENCOND expresion CLOSECOND'''
    pass
    pilaO.push(p[1])
    if values.size() >= 1:
        global counter,temp_counter
        valor = values.pop()
        values.push("escrita")
        tipo ="escrita"
        operizq =pOper.pop()
        operador = pilaO.pop()
        respuesta_semantica = operacion_compatible(operador,valor,tipo)
        global build_errors
        if respuesta_semantica == "":
            dir_izq=obtener_direccion(operizq)
            dir_temp = obtener_direccion("temp"+str(temp_counter))
        else:
            dir_izq=obtener_direccion(operizq)
            dir_temp = obtener_direccion("temp"+str(temp_counter))
            build_errors.append(respuesta_semantica)
        pOper.push("temp"+str(temp_counter))
        temp_counter+=1
        cuadruplos[counter] = [operador,dir_izq,"",dir_temp]
        counter+=1
##Start of control/decision expresions
##-----------------------------------------------
def p_laberinto(p):
    '''laberinto : laberinto3 laberinto1 laberinto2 varcte'''
    pass
    if values.size() >= 1:
        global counter,temp_counter
        valor = values.pop()
        tipo = types.pop()
        operation = operations.pop()
        operadorizq=pOper.pop()
        operador=pOper.pop()
        global build_errors
        ##Checks semantics
        respuesta_semantica = operacion_compatible(operation,tipo,valor)
        if respuesta_semantica == "":
            dir_izq = obtener_direccion(operadorizq)
            dir_der = obtener_direccion(operador)
            dir_temp = obtener_direccion("temp"+str(temp_counter))
        else:
            build_errors.append(respuesta_semantica)
        #Creates structure of operators for vm
        temp_counter+=1
        cuadruplos[counter]=[operation,dir_izq,dir_der,dir_temp]
        counter+=1
        #In case of a negative operator
        if not negative.isEmpty():
            dir_temp2 = obtener_direccion("temp"+str(temp_counter))
            cuadruplos[counter]=[negative.pop(),dir_temp,"",dir_temp2]
            temp_counter+=1
            dir_temp = dir_temp2
            counter+=1
        pSaltos.push(counter)
        #Constructor of logic operator
        cuadruplos[counter]=["gotof",dir_temp,"",""]
        counter+=1
#Language own boolean reserved words        
def p_laberinto1(p):
    '''laberinto1 : PAREDDERECHA
                | PAREDIZQUIERDA
                | PAREDARRIBA
                | PAREDABAJO
		| LIBREDERECHA
                | LIBREIZQUIERDA
                | LIBREABAJO
                | LIBREARRIBA
		| METADERECHA
                | METAIZQUIERDA
                | METAARRIBA
                | METAABAJO'''
    pass
    types.push("decision")
    pOper.push(p[1])
#Comparison operators
def p_laberinto2(p):
    '''laberinto2 : DIFERENTEA
	| IGUALA'''
    pass
    operations.push(p[1])
def p_laberinto3(p):
    '''laberinto3 : NOT
                   | '''
    pass
    if len(p) > 1:
        negative.push(p[1])
##Regular expresions start
##----------------------------------------------------
def p_expresion(p):
    '''expresion : termino exp'''
    pass 
#Specific error generation
def p_expresion_error(p):
    '''expresion : error exp'''
    global build_errors
    build_errors.append("Error: Operacion matematica incorrecta")
def p_exp(p):
    '''exp :
            | exp2 exp'''
    pass
#Sums and substractions
def p_exp2(p):
    '''exp2 : RESTA termino 
            | SUMA termino'''
    pass
    pilaO.push(p[1])
    if pilaO.top() == "+" or pilaO.top() == "-":
        global counter,temp_counter
        operador = pilaO.pop()
        operDer = pOper.pop()
        operIzq = pOper.pop()
        #Construction of structure for operations on vm
        dir_der = obtener_direccion(operDer)
        dir_izq = obtener_direccion(operIzq)
        dir_temp = obtener_direccion("temp"+str(temp_counter))
        pOper.push("temp"+str(temp_counter))
        temp_counter+=1
        cuadruplos[counter] = [operador,dir_izq,dir_der,dir_temp]
        counter+=1
#Start of term definition
#----------------------------------------------------
def p_termino(p):
    '''termino : varcte termino2'''
    pass
def p_termino2(p):
    '''termino2 : 
                | termino3 termino2'''
    pass
 #Divition and multiplication   
def p_termino3(p):
    '''termino3 : DIVISION varcte
                | MULTIPLICACION varcte'''
    pass
    pilaO.push(p[1])
    if pilaO.top() == "*" or pilaO.top() == "/":
        global counter,temp_counter
        #To keep consistency in stacks
        operador = pilaO.pop()
        operDer = pOper.pop()
        operIzq = pOper.pop()
        #For operations
        dir_der = obtener_direccion(operDer)
        dir_izq = obtener_direccion(operIzq)
        dir_temp = obtener_direccion("temp"+str(temp_counter))
        pOper.push("temp"+str(temp_counter))
        temp_counter+=1
        cuadruplos[counter] = [operador,dir_izq,dir_der,dir_temp]
        counter+=1
#Start of types and constants
#-----------------------------------------
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
    global build_errors
    if p:
        build_errors.append("Error de escritura cerca de '%s'" % p.value)
        build_errors.append("En linea %i"%p.lineno)
                
    else:
        if not braces.isEmpty():
            build_errors.append("Error: Falta '}' o ')'")
        build_errors.append("Error de escritura al final del archivo")




import sys
class Scanner(object):
    def __init__(self, entrada):
        self.entrada = entrada
    def scan(self):
        global build_errors,cuadruplos,ids,temp_counter,counter,types,operations,values,pOper,pilaO,braces,pSaltos
        #Lex construction
        import ply.lex as lex
        lex.lex()
        #Sintax construction
        import ply.yacc as yacc
        yacc.yacc()
        del build_errors[:]
        #Structure cleaning
        ids.dispatch()
        types.dispatch()
        operations.dispatch()
        values.dispatch()
        pOper.dispatch()
        pilaO.dispatch()
        braces.dispatch()
        pSaltos.dispatch()
        cuadruplos.clear()
        temp_counter = 0
        counter = 0
        #Compiling entry
        yacc.parse(self.entrada)
        #Return the build error's array or null in case there weren't any
        return build_errors
 
