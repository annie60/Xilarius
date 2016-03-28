# Xilarius

## Autoras
##### Ana Arellano Palacios A01089996
##### Ana Karen Reyna A01280310

## Descripción
Compilador y maquina virtual para lenguaje Xilarius.

Este lenguaje se compone de una interfaz gráfica donde el niño vera a Xilarius (personaje principal del sistema), 

una meta y un sección para introducir los bloques de instrucciones que quiera que Xilarius realice. 

Las instrucciones deberán de generar como resultado que Xilarius llegue a la meta propuesta.

Proyecto final para clase de Diseño de compiladores.

__Prof. Elda Quiroga__

__Dr. José Icaza__

## Requisitos
- Python V.3.5.x
- [PLY](https://github.com/dabeaz/ply) v.3.8
- Libreria [Pygame](http://www.pygame.org/) V.3.X
- Libreria [Tygame](http://www.pygame.org/project-Tygame+-+GUI+Project-2081-.html)

## Como ejecutar?
#### Funcion de escaner y analizador
- Usar archivo __input.txt__ para diseñar un programa 'dummy'
- En la consola ejecutar
` python scaner_parser.py input.txt `

#### Interfaz Grafica
- En la consola ejecutar
` python main.py `

## Notas
* Este proyecto esta probado correctamente para sistema operativo windows, cualquier otro sistemas podria tener fallas.
* Hubo cambios a la libreria tygame, en epecifico el archivo __main.py__ ,por lo que se tiene que tomar del directorio local en este repositorio.
* La base para la interfaz grafica del laberinto se tomo del codigo compartido en [Bipo Maze](http://www.pygame.org/project-Bipo+Maze-2159-.html)
