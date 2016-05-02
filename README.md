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
- Libreria [PGU](https://github.com/parogers/pgu)

## Como ejecutar?

#### Interfaz Grafica y maquina virtual
- En la consola ejecutar
` python main.py `
- Presionar __'Principiante'__ o __'Experto'__
- Crear programa
    * Teclear programa en la pantalla de texto y presionar __'Guardar'__ .
    * O bien seleccionar la opción __"Archivo"__ y __"Abrir"__ para seleccionar un archivo __.txt__ con código.
- Presionar __'Paso 1'__
- Presionar __'Paso 2'__

#### Estructuras basicas de un programa
Revisar [Wiki](https://github.com/annie60/Xilarius/wiki/Sintaxis y lexico) para obtener léxico y sintaxis correctos.
##### Layout __obligatorio__

```
miPrograma Primerprograma;
{
    crearPersonaje Minombre;
    ...
}
```
##### Declaración de variables
```
    var Mivar escrita = "hola";
```
##### Asignación de valores
```
    Mivar = hacerEscrita(3);
    Miotravar = 5*7-1;
```
##### Condiciones
```
    siEs (paredDerecha == verdadero){
    ...
    }
```

```
    siEs(no libreIzquieda == verdadero){
    ...
    }
```
##### Ciclos
```
    repetirMientras(libreAbajo <> falso){
    ...
    }
```
##### Funciones propias
```
    Minombre.atras(1);
    Minombre.adelante(3*2+6);
    Minombre.responder("hola");
    Minombre.parar;
```
## Notas
* Este proyecto esta probado correctamente para sistema operativo **Windows**, cualquier otro sistema podria tener fallas.
* Hubo cambios a la librería tygame, en epecífico el archivo __main.py__ ,por lo que se tiene que tomar del directorio local en este repositorio.
* Hubo cambios en la librería pgu-gui, el archivo __textarea.py__ tiene que tomarse del repositorio.
* La base para la interfaz grafica del laberinto se tomo del codigo compartido en [Bipo Maze](http://www.pygame.org/project-Bipo+Maze-2159-.html)

## Licencia

    Copyright (C) 2016  Ana Karen Reyna and Ana Gpe. Arellano Palacios

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see http://www.gnu.org/licenses.
