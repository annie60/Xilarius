# -----------------------------------------------------------------------------
# Semantic analysis: Xilarius
# Project
# Ana Arellano   		A01089996
# Ana Karen Reyna		A01280310
# -----------------------------------------------------------------------------
#Class to support the construction of semantic structures
class Stack:
     def __init__(self):
         self.items = [] 
     def isEmpty(self):
         return self.items == [] #list empty? T|F
     def top(self): #Top element of list
         return self.items[len(self.items)-1]
     def push(self, item):
         self.items.append(item) 
     def pop(self):
         return self.items.pop() 
     def size(self):
         return len(self.items)
     def dispatch(self): #Cleans structure
         del self.items[:]
#Class to support construction of semantic structures
class Queue:
    def __init__(self):
        self.items =[]
    def isEmpty(self):
        return self.items ==[]
    def top(self): #Return top element
         return self.items[len(self.items)-1]
    def enqueue(self,item): 
        self.items.insert(0,item)
    def dequeue(self): 
        return self.items.pop()
    def size(self):
        return len(self.items)
    def dispatch(self): #Cleans structure
        del self.items[:]
#Dictionary
# Use of global variables ONLY
# Dictionary definition
# { "nombre" : (value,constantType,virtualDirection)}
var_dicc_funciones = {}
#Helper structures
#Constants {memoryDirection :  value}
const_mem={}
const_mem_output={}
temp_mem = {}
temp_mem_output= {}
global_mem_output= {}
#Virutal memory counters
global_mem_counter = 1000
temp_mem_counter = 20000
const_mem_counter = 25000
#Operators, types and reserve words definition
var_boleanas = ("verdadero","falso")
var_tipos = ("numero","escrita","decision","personaje")
var_operaciones = ("=","+","-","*","/","<>","==","parar","responder","arriba","abajo","derecha","izquierda","hacerEscrita")
var_constantes = ("verdadero","falso","paredDerecha","paredIzquierda","paredArriba","paredAbajo","libreDerecha","libreIzquierda","libreArriba","libreAbajo","metaDerecha","metaIzquierda","metaArriba","metaAbajo")
#Semantics cube format
#                       =       +       -       *       /       <>      ==      p   r   at  ad   d   i   conv
#numero     numero      1       1       1       1       1       -1      -1     -1  -1  -1   -1  -1  -1   -1
#numero     escrita     -1      -1      -1      -1      -1      -1      -1     -1  -1  -1   -1  -1  -1    1
#numero     decision    -1      -1      -1      -1      -1      -1      -1     -1  -1  -1   -1  -1  -1   -1
#numero     personaje   -1      -1      -1      -1      -1      -1      -1     -1  -1   1    1   1   1   -1
#escrita    numero      -1      -1      -1      -1      -1      -1      -1     -1  -1  -1   -1  -1  -1   -1
#escrita    escrita      1      -1      -1      -1      -1      -1      -1     -1  -1  -1   -1  -1  -1   -1
#escrita    decision    -1      -1      -1      -1      -1      -1      -1     -1  -1  -1   -1  -1  -1   -1
#escita     personaje   -1      -1      -1      -1      -1      -1      -1     -1   1  -1   -1  -1  -1   -1
#decision   numero      -1      -1      -1      -1      -1      -1      -1     -1  -1  -1   -1  -1  -1   -1
#decision   escrita     -1      -1      -1      -1      -1      -1      -1     -1  -1  -1   -1  -1  -1    1
#decision   decision     1      -1      -1      -1      -1       1       1     -1  -1  -1   -1  -1  -1   -1
#decision   personaje   -1      -1      -1      -1      -1      -1      -1     -1  -1  -1   -1  -1  -1   -1
#personaje  numero      -1      -1      -1      -1      -1      -1      -1     -1  -1   1    1   1   1   -1
#personaje  escrita     -1      -1      -1      -1      -1      -1      -1     -1   1  -1   -1  -1  -1   -1
#personaje  decision    -1      -1      -1      -1      -1      -1      -1     -1  -1  -1   -1  -1  -1   -1
#personaje  personaje    1      -1      -1      -1      -1      -1      -1      1  -1  -1   -1  -1  -1   -1

cubo_semantico = (
    ((1,1,1,1,1,-1,-1,-1,-1,-1,-1,-1,-1,-1),
    (-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,1),
    (-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1),
    (-1,-1,-1,-1,-1,-1,-1,-1,-1,1,1,1,1,-1)
    ),
    ((-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1),
    (1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1),
    (-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1),
    (-1,-1,-1,-1,-1,-1,-1,-1,1,-1,-1,-1,-1,-1)
    ),
    ((-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1),
    (-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,1),
    (1,-1,-1,-1,-1,1,1,-1,-1,-1,-1,-1,-1,-1),
    (-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1)
    ),
    ((-1,-1,-1,-1,-1,-1,-1,-1,-1,1,1,1,1,-1),
    (-1,-1,-1,-1,-1,-1,-1,-1,1,-1,-1,-1,-1,-1),
    (-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1),
    (1,-1,-1,-1,-1,-1,-1,1,-1,-1,-1,-1,-1,-1)
    )
    ) 
#Function's table definition, initializes main dictionary of globals
#is a void function
def crear_modulo(nombre,ambiente):
    global var_dicc_funciones
    var_dicc_funciones[ambiente] = (nombre,{})

#Creates variable's table, adding the information to the dictionary
#Gets the name, type and value (all strings)
#and returns a string, null if there weren’t any mistakes
def agregar_variable(nombre,valor,tipo):
    #Checks if the name is already in use
    if existe_variable(nombre):
        return "Error: Nombre de variable '"+nombre+"' repetido"
        
    else:
        #Checks that the assignment of the value 
        #has consistency with the type of variable
        if operacion_compatible("=",tipo,valor) == "":
            global global_mem_output,var_dicc_funciones,global_mem_counter
            var_dicc_funciones["miPrograma"][1][nombre]=(valor,tipo,global_mem_counter)
            global_mem_output[global_mem_counter] = valor
            global_mem_counter+=1
            return ""
        else:
            return "Error: Asignacion a '"+nombre+"' no compatible"

#Transforms string value to index of type's array
def convertir_valor(valor):
        if valor.isdigit():
            return 0
        elif isinstance(valor,str) and not(valor in var_boleanas) and ('"' in valor):
            return 1
        elif (valor in var_boleanas):
            return 2
        elif (valor in var_dicc_funciones["miPrograma"][1]):
            atributos =var_dicc_funciones["miPrograma"][1][valor]
            return var_tipos.index(atributos[1])
        elif valor == "personaje":
            return 3
        elif valor in var_tipos:
            return var_tipos.index(valor)
        else:
            return -1

#Defines compatibility between types and operations
#according to the semantics cube defined previously
#Receives operation and the two types involve, all strings
# and returns a string, null if there weren’t any mistakes
def operacion_compatible(operacion, tipouno,tipodos):
    #Gets information from parser
    tipo=convertir_valor(tipouno)
    indiceValor = convertir_valor(tipodos)
    operador =var_operaciones.index(operacion)
    if indiceValor >= 0 and tipo >=0 :
        if (cubo_semantico[tipo][indiceValor][operador] == 1):
            return ""
        else: #Non compatible operation
            if tipo == indiceValor:
                return "Error: "+var_tipos[indiceValor]+" no es compatible con operacion "+operacion
            else:
                return "Error: Tipos "+var_tipos[tipo]+" y "+var_tipos[indiceValor]+" no son compatibles con operacion "+operacion
    elif tipo < 0: #Variable not found
        return "Error: Variable '"+tipouno+"' no declarada"
    else:
        return "Error:Variable '"+tipodos+"' no declarada"

#Translates to virtual memory numbers or unique pointers
#receives a string and returns an integer 
def obtener_direccion(variable):
    global temp_mem,global_mem_counter,temp_mem_counter,const_mem_counter
    #Checks if variable is global,constant or temporary
    if (variable in var_dicc_funciones["miPrograma"][1]): 
        return var_dicc_funciones["miPrograma"][1][variable][2]
    elif isinstance(variable,int) or variable.isdigit() or (variable in var_constantes):
        #If it already exists then just return 
        #the memory direction associated
        if (variable in const_mem):
            return const_mem[variable]
        else:
        #If it doesn't exists then it creates the space
        #and returns the memory direction used
            crear_constante(variable)
            return (const_mem_counter - 1)
        
    else:
        #If it doesn't exists then it creates the space
        #and returns the memory direction used
        if not (variable in temp_mem):
            crear_temporal(variable)
            return (temp_mem_counter - 1)
        else:
        #If it already exists then just return 
        #the memory direction associated
            return temp_mem[variable]
        
#Checks for previous name declaration
#meaning is a repeated variable name use
def existe_variable(nombre):
    global var_dicc_funciones
    if nombre in var_dicc_funciones["miPrograma"][1] :
        return True
    else:
        return False

#Helper function to create specific constant slot of memory
def crear_constante(valor):
    global const_mem,const_mem_counter
    const_mem[valor]=const_mem_counter
    const_mem_output[const_mem_counter] =valor
    const_mem_counter+=1

#Helper function to create specific temporary slot of memory
def crear_temporal(valor):
    global temp_mem,const_mem_output,temp_mem_counter
    temp_mem[valor]=temp_mem_counter
    temp_mem_output[temp_mem_counter]=valor
    temp_mem_counter+=1

#Generates intermediate code file
#Is a void function
def crear_archivo_salida(cuadruplos):
    global const_mem_output,temp_mem_output,global_mem_output,const_mem,temp_mem,global_mem_counter,temp_mem_counter,const_mem_counter
    file = open('result.txt','w')
    #Creates blocks delimited by '$' in between each section
    file.write(str(global_mem_output))
    file.write('$')
    file.write(str(const_mem_output))
    file.write('$')
    file.write(str(temp_mem_output))
    file.write('$')
    file.write(str(cuadruplos))
    #Cleanup
    var_dicc_funciones.clear()
    const_mem.clear()
    const_mem_output.clear()
    temp_mem.clear()
    temp_mem_output.clear()
    global_mem_output.clear()
    #Restart of counters
    global_mem_counter = 1000
    temp_mem_counter = 20000
    const_mem_counter = 25000
