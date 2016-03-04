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
         #metodo append nativo en python
         #append(elemento): agrega un elemento
         #al inicio de la lista
         self.items.append(item) 
     def pop(self):
         #metodo pop nativo en python
         #pop(indice): elimina el objeto que se encuentre
         #al inicio o bien que este en la posicion del indice
         #por lo tanto el indice es opcional
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
        #Metodo nuevo preimplementado en python
        #insert(indice,elemento): agrega un elemento
        #a la lista en el indice que se le especifica
        #en este caso siempre debe de ir 'al final' de la fila
        self.items.insert(0,item)
    def dequeue(self): #Sacar elemento de una fila
    #Uso del mismo metodo pop() pre implementado en Python
        return self.items.pop()
    def size(self):
        return len(self.items)
#Diccionario
# Uso de variables globales solamente
# Definicion de un diccionario con llaves y una lista de atributos
# { "nombre" : (valor,tipoDeCte)}
var_globales = {}

     
def agregar_variable(nombre,valor,tipo):
    if existe_variable(nombre):
        print("Error: Nombre de variable repetido")
        return False
    else:
        if asignacion_compatible(tipo,valor):
            global var_globales
            var_globales[nombre]=(valor,tipo)
            print(var_globales)
            return True
        else:
            print("Asignacion no compatible")
            return False
def asignacion_compatible(tipo, valor):
    if tipo == "numero" : 
        if not(c.isalpha() for c in valor):#TODO algo para identificar solo numeros
            return True
        else:
            print("Error: Esta tipo "+tipo+" no puede tener este tipo de valor "+valor)
            return False
    elif tipo == "escrita":
        if isinstance(valor,basestring) and not(valor == "falso" or valor == "verdadero"):
            print(valor)
            return True
        else:
            print("Error: Esta variable "+tipo+" no puede tener este valor "+valor)
            return False
    elif tipo == "decision":
        if (valor == "verdadero" or valor == "falso"):
            
            return True
        else:
            print("Error: Esta variable "+tipo+" no puede tener este valor "+valor)
            return False
    else:
        return False    
def operacion_compatible(operacion, variableuno,variabledos):
    #TODO
    print ("Error: Esta variable no puede tener este tipo de valor")
    return true
def es_compatible(variableuno,variabledos):
    global var_globales
    tipoUno = var_globales[variableuno][1]
    tipoDos = var_globales[variabledos][1]
    if tipoUno == tipoDos:
        return True
    else:
        print("Error: Tipos "+tipoUno+" y "+tipoDos+" no son compatibles ")
        return False
def existe_variable(nombre):
    global var_globales
    if nombre in var_globales:
        return True
    else:
        return False


