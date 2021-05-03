''' Crea un pequeño sistema para gestionar los platos del menú de un restaurante. 
Por ahora debes empezar creando un script llamado restaurante.py y dentro una función crear_bd() 
que creará una pequeña base de datos restaurante.db con las siguientes dos tablas:

CREATE TABLE categoria(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre VARCHAR(100) UNIQUE NOT NULL)

CREATE TABLE plato(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre VARCHAR(100) UNIQUE NOT NULL, 
                categoria_id INTEGER NOT NULL,
                FOREIGN KEY(categoria_id) REFERENCES categoria(id))

Nota: La línea FOREIGN KEY(categoria_id) REFERENCES categoria(id) indica un tipo de clave especial (foránea), 
por la cual se crea una relación entre la categoría de un plato con el registro de categorías.

Llama a la función y comprueba que la base de datos se crea correctamente.

Crea una función llamada agregar_categoria() que pida al usuario un nombre de categoría y se encargue de crear 
la categoría en la base de datos (ten en cuenta que si ya existe dará un error, por que el nombre es UNIQUE).

Ahora, crea un pequeño menú de opciones dentro del script, que te de la bienvenida al sistema y te permita 
crear una categoría o Salir. Añade las siguientes tres categorías utilizando este menú de opciones:

- Primeros
- Segundos
- Postres

Crea una función llamada agregar_plato() que muestre al usuario las categorías disponibles y le permita escoger una 
(escribiendo un número).

Luego le pedirá introducir el nombre del plato y lo añadirá a la base de datos, teniendo en cuenta que 
la categoria del plato concuerde con el id de la categoría y que el nombre del plato no puede repetirse 
(no es necesario comprobar si la categoría realmente existe, en ese caso simplemente no se insertará el plato).

Agrega la nueva opción al menú de opciones y añade los siguientes platos:

Primeros: Ensalada del tiempo / Zumo de tomate
Segundos: Estofado de pescado / Pollo con patatas
Postres: Flan con nata / Fruta del tiempo

Crea una función llamada mostrar_menu() que muestre el menú con todos los platos de forma ordenada: 
los primeros, los segundos y los postres. Optativamente puedes adornar la forma en que muestras el menú por pantalla
'''

import sqlite3

def crear_bd():
	connection = sqlite3.connect("restaurante.db")

	connection.execute('''
		CREATE TABLE IF NOT EXISTS categoria(
		    id INTEGER PRIMARY KEY AUTOINCREMENT,
		    nombre VARCHAR(100) UNIQUE NOT NULL
		)
		''')

	connection.execute('''
		CREATE TABLE IF NOT EXISTS plato(
		    id INTEGER PRIMARY KEY AUTOINCREMENT,
		    nombre 	VARCHAR(100) UNIQUE NOT NULL,
		    categoria_id INTEGER NOT NULL,
		    FOREIGN KEY(categoria_id) REFERENCES categoria(id)
		)
		''')

	connection.commit()
	connection.close()
    
def mostrar_menu():
    connection = sqlite3.connect("restaurante.db") 
    cursor = connection.cursor() 
    cursor.execute("SELECT categoria_id, nombre FROM plato ORDER BY categoria_id")
    platos = cursor.fetchall()
    
    primeros = "Primeros: "
    segundos = "Segundos: "
    postres = "Postres: "
    
    for plato in platos:
        if plato[0] == 1:
            primeros = primeros + plato[1] + " / "
        if plato[0] == 2:
            segundos = segundos + plato[1] + " / "
        if plato[0] == 3:
            postres = postres + plato[1] + " / "
        
            
    print(primeros,"\n",segundos,"\n",postres,"\n")
    

def agregar_categoria():
    opcion = 0
    nomcategoria = ""
    print("Agregar categoría") 
    print("=================") 
    print("1 --> primeros") 
    print("2 --> segundos") 
    print("3 --> postres") 
    opcion = int(input("opción:"))
    if opcion >= 1 and opcion <= 3:
        if opcion == 1:
            nomcategoria = [("Primeros")]
        if opcion == 2:
            nomcategoria = [("Segundos")]
        if opcion == 3:
            nomcategoria = [("Postres")]
          
        connection =sqlite3.connect("restaurante.db")
        cursor = connection.cursor()       
        
        try:
            cursor.execute("INSERT INTO categoria VALUES(null,?)",nomcategoria) 
        except:
            connection.rollback()
            connection.close()
        else:
            connection.commit()
            connection.close()
                

def agregar_plato(): 
    existe = False
    print("\nAgregar plato")
    print("=============")
    connection = sqlite3.connect("restaurante.db") 
    cursor = connection.cursor() 
    cursor.execute("SELECT * FROM categoria")
    categorias = cursor.fetchall()
    
    for categoria in categorias:
        print(categoria[0]," --> ", categoria[1])
    
    opcion = int(input("Escoge una categoría:"))
    
    for categoria in categorias:
        if categoria[0] == opcion:
            existe = True


    if existe:
        correcto = False
        
        while correcto == False:
            nomplato = str(input("Introduce nombre del plato:"))
            if nomplato == "":
                print("Debe introducir un nombre de plato\n")
                correcto = false
                connection.rollback()
            else:
                plato=[(nomplato),(opcion)]
                cursor.execute("INSERT INTO plato VALUES(null,?,?)",plato)
                connection.commit()
                connection.close
                correcto = True
                
    else:
        print("No existe esa categoría")

# Creamos las BB.DD
crear_bd()

#Creamos categorias
agregar_categoria()

#Creamos platos
agregar_plato()

#mostramos los menús
mostrar_menu()