# -----------------------------------------------------------------------------
# Analisis semantico de variables y funciones: Xilarius
# Proyecto
# Ana Arellano   		A01089996
# Ana Karen Reyna		A01280310
# -----------------------------------------------------------------------------
#Clase pila para apoyo en la construccion de tablas
class Stack:
     def __init__(self):
         self.items = [] #inicializa una lista vacia

     def isEmpty(self):
         return self.items == [] #esta vacia la lista T|F
     def top(self):
         return self.items[len(self.items)-1]
     def push(self, item):
         self.items.append(item) 
     def pop(self):
         return self.items.pop() 
     def size(self):
         #Regresa el numero de elementos en la lista
         return len(self.items)
#Fila
class Queue:
    def __init__(self):
        self.items =[]
    def isEmpty(self):
        return self.items ==[]
    def top(self):
         return self.items[len(self.items)-1]
    def enqueue(self,item): #Agregar elemento a la lista
        self.items.insert(0,item)
    def dequeue(self): #Sacar elemento de una fila
        return self.items.pop()
    def size(self):
        return len(self.items)
#Diccionario
# Uso de variables globales solamente
# Definicion de un diccionario con llaves y una lista de atributos
# { "nombre" : (valor,tipoDeCte)}
var_dicc_funciones = {}

var_boleanas = ("verdadero","falso")
var_tipos = ("numero","escrita","decision","personaje")
var_operaciones = ("=","+","-","*","/","<>","==","parar","responder","atras","adelante","derecha","izquierda")
#Formato de matriz para cubo
#                       =       +       -       *       /       <>      ==      p   r   at  ad   d   i
#numero     numero      1       1       1       1       1       -1      -1     -1  -1  -1   -1  -1  -1
#numero     escrita     -1      -1      -1      -1      -1      -1      -1     -1  -1  -1   -1  -1  -1   
#numero     decision    -1      -1      -1      -1      -1      -1      -1     -1  -1  -1   -1  -1  -1
#numero     personaje   -1      -1      -1      -1      -1      -1      -1     -1  -1   1    1   1   1
#escrita    numero      -1      -1      -1      -1      -1      -1      -1     -1  -1  -1   -1  -1  -1   
#escrita    escrita      1      -1      -1      -1      -1      -1      -1     -1  -1  -1   -1  -1  -1   
#escrita    decision    -1      -1      -1      -1      -1      -1      -1     -1  -1  -1   -1  -1  -1
#escita     personaje   -1      -1      -1      -1      -1      -1      -1     -1   1  -1   -1  -1  -1
#decision   numero      -1      -1      -1      -1      -1      -1      -1     -1  -1  -1   -1  -1  -1  
#decision   escrita     -1      -1      -1      -1      -1      -1      -1     -1  -1  -1   -1  -1  -1   
#decision   decision     1      -1      -1      -1      -1       1       1     -1  -1  -1   -1  -1  -1
#decision   personaje   -1      -1      -1      -1      -1      -1      -1     -1  -1  -1   -1  -1  -1
#personaje  numero      -1      -1      -1      -1      -1      -1      -1     -1  -1   1    1   1   1
#personaje  escrita     -1      -1      -1      -1      -1      -1      -1     -1   1  -1   -1  -1  -1
#personaje  decision    -1      -1      -1      -1      -1      -1      -1     -1  -1  -1   -1  -1  -1
#personaje  personaje    1      -1      -1      -1      -1      -1      -1      1  -1  -1   -1  -1  -1

cubo_semantico = (
    ((1,1,1,1,1,-1,-1,-1,-1,-1,-1,-1,-1),
    (-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1),
    (-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1),
    (-1,-1,-1,-1,-1,-1,-1,-1,-1,1,1,1,1)
    ),
    ((-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1),
    (1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1),
    (-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1),
    (-1,-1,-1,-1,-1,-1,-1,-1,1,-1,-1,-1,-1)
    ),
    ((-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1),
    (-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1),
    (1,-1,-1,-1,-1,1,1,-1,-1,-1,-1,-1,-1),
    (-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1)
    ),
    ((-1,-1,-1,-1,-1,-1,-1,-1,-1,1,1,1,1),
    (-1,-1,-1,-1,-1,-1,-1,-1,1,-1,-1,-1,-1),
    (-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1),
    (1,-1,-1,-1,-1,-1,-1,1,-1,-1,-1,-1,-1)
    )
    ) 
def crear_modulo(nombre,ambiente):
    global var_dicc_funciones
    var_dicc_funciones[ambiente] = (nombre,{})
#Funcion para crear 'tabla' de variables
def agregar_variable(nombre,valor,tipo):
    #Revisa que no este repetida la variable
    if existe_variable(nombre):
        print("Error: Nombre de variable repetido")
        return False
    else:
        #Revisa que la asignacion que se le hace sea
        #correspondiente al tipo de variable que es
        if operacion_compatible("=",tipo,valor):
            global var_dicc_funciones
            var_dicc_funciones["miPrograma"][1][nombre]=(valor,tipo)
            return True
        else:
            print("Error: Asignacion no compatible")
            return False

def convertir_valor(valor):
    #Convierte valores a tipo numericos
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
        else:
            print ("Error:Variable '"+valor+"' no declarada")
            return -1
          
def operacion_compatible(operacion, tipouno,tipodos):
    #Obtiene la informacion del parser
    tipo=var_tipos.index(tipouno)
    indiceValor = convertir_valor(tipodos)
    operador =var_operaciones.index(operacion)
    if indiceValor >= 0:
        if (cubo_semantico[tipo][indiceValor][operador] == 1):
            return True
        else:
            print("Error: Tipos "+var_tipos[tipo]+" y "+var_tipos[indiceValor]+" no son compatibles con operacion "+operacion)
            return False
    else:
        return False
def operacion(operacion, tipouno,tipodos):
    #Obtiene la informacion del parser
    tipo=convertir_valor(tipouno)
    indiceValor = convertir_valor(tipodos)
    operador =var_operaciones.index(operacion)
    if indiceValor >= 0:
        if (cubo_semantico[tipo][indiceValor][operador] == 1):
            return True
        else:
            print("Error: Tipos "+var_tipos[tipo]+" y "+var_tipos[indiceValor]+" no son compatibles con operacion "+operacion)
            return False
    else:
        return False

def existe_variable(nombre):
    global var_dicc_funciones
    if nombre in var_dicc_funciones["miPrograma"][1] :
        return True
    else:
        return False

def cuadruplo(operador,operandoizq,operandoder):
    indice = var_operaciones.index(operador)
    if operandoizq in var_dicc_funciones["miPrograma"][1]:
        operandoizq=var_dicc_funciones["miPrograma"][1][operandoizq][0]
    if operandoder in var_dicc_funciones["miPrograma"][1]:
        operandoder=var_dicc_funciones["miPrograma"][1][operandoder][0]
    if indice == 1:
        return int(operandoizq) + int(operandoder)
    elif indice == 2:
        return int(operandoizq) - int(operandoder)
    elif indice == 3:
        return int(operandoizq) * int(operandoder)
    elif indice == 4:
        return int(int(operandoizq) / int(operandoder))
        