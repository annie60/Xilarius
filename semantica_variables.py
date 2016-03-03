# -----------------------------------------------------------------------------
# Analisis semantico de variables: Xilarius
# Proyecto
# Ana Arellano   		A01089996
# Ana Karen Reyna		A01280310
# -----------------------------------------------------------------------------

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
        var_globales[nombre]=(valor,tipo)
        return True
def asignacion_compatible(variable, valor):
    #TODO
    print ("Error: Esta variable no puede tener este tipo de valor")
    return true
def es_compatible(variableuno,variabledos):
    tipoUno = var_globales[variableuno][1]
    tipoDos = var_globales[variabledos][1]
    if tipoUno == tipoDos:
        return True
    else:
        print("Error: Tipos "+tipoUno+" y "+tipoDos+" no son compatibles ")
        return False
def existe_variable(nombre):
    if nombre in var_globales:
        return True
    else:
        return False
#Pruebas
#Posiblemente se cambie el tipo por  algo numerico no string
print(agregar_variable("mi",2,"numero"))
print(agregar_variable("mi2",4,"numero"))
print(es_compatible("mi","mi2"))
print(var_globales)
