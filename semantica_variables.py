# -----------------------------------------------------------------------------
# Analisis semantico de variables: Xilarius
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
var_globales = {}
var_boleanas = ("verdadero","falso")
#Funcion para crear 'tabla' de variables
def agregar_variable(nombre,valor,tipo):
    #Revisa que no este repetida la variable
    if existe_variable(nombre):
        print("Error: Nombre de variable repetido")
        return False
    else:
        #Revisa que la asignacion que se le hace sea
        #correspondiente al tipo de variable que es
        if asignacion_compatible(tipo,valor):
            global var_globales
            var_globales[nombre]=(valor,tipo)
            return True
        else:
            print("Asignacion no compatible")
            return False
#TODO: Crear cubo de operaciones semanticas para remplazar operacion y asignacion
def asignacion_compatible(tipo, valor):
    #Revisa para los tres tipos de ctes. los valores posibles
    if tipo == "numero" : 
        if valor.isdigit():
            return True
        else:
            print("Error: Esta variable tipo '"+tipo+"' no puede tener este valor "+valor)
            return False
    elif tipo == "escrita":
        if isinstance(valor,basestring) and not(valor == "falso" or valor == "verdadero"):
            print(valor)
            return True
        else:
            print("Error: Esta variable tipo '"+tipo+"' no puede tener este valor "+valor)
            return False
    elif tipo == "decision":
        if (valor in var_boleanas):
            return True
        else:
            print("Error: Esta variable tipo '"+tipo+"' no puede tener este valor "+valor)
            return False
    else:
        return False    
def operacion_compatible(operacion, tipouno,tipodos):
    #Obtiene la informacion del parser
    if tipouno == tipodos:
        if operador_compatible(operacion,tipouno):
            return True
        else:
            print("Error: Tipo de operacion no compatible ")
            return False
    else:
        print("Error: Tipos "+tipoUno+" y "+tipoDos+" no son compatibles ")
        return False
    
def comparacion_compatible(operandoizq):
    #Obtiene la informacion del parser
        if operandoizq in var_boleanas:
            return True
        elif existe_variable(operandoizq):
            global var_globales
            
            if var_globales[operandoizq][1] == "decision":
                return True
            else:
                return False
        else:
            print("Error: Variable  '"+operandoizq+"' en comparacion no declarada")
            return False

def existe_variable(nombre):
    global var_globales
    if nombre in var_globales:
        return True
    else:
        return False


