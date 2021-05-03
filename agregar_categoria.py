# -*- coding: utf-8 -*-
from tkinter import *
import sqlite3
from tkinter import messagebox

# Compruebo la BBDD. Si no existe la crea
def crear_bd():
    #Abro la conexión
	connection = sqlite3.connect("restaurante.db")

    #Creo un cursor
	cursor = connection.cursor()

    #Creo las tablas categoria y plato
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

    #Guardo los cambios
	connection.commit()
    #Cierro la conexión
	connection.close()

	


class Application(Frame):
    #Constructor
    def __init__(self, master=None):
    	super().__init__(master=None)
    	self.master = master
    	self.master.title("Carta del Restaurante")
    	self.master.config()

        # Ejecuto la función por si no existiera la BBDD
    	crear_bd()

        #Llamo a la función que creará los widgets
    	self.create_widgets()

    # Función que insertará la categoría en BBDD.
    def agregar_categoria(self):
        nomcategoria=""
        result=""

        #Abro la conexión
        connection = sqlite3.connect("restaurante.db")

        #Creo un cursor
        cursor = connection.cursor()

        #Si la opción elegida es la de "Primeros"...
        if self.opcion.get() == 1:    
            #Hago un select para saber si ya existe la categoria de "primeros"
            cursor.execute("SELECT * FROM categoria WHERE id == 1")
            resul = cursor.fetchone()

            #Si no existe, establezco la categoría. Si existe muestro mensaje de aviso
            if resul == None:
                nomcategoria = [("Primeros")]
            else:
                messagebox.showinfo("Alerta","Ya existe la categoría de primeros platos")

        if self.opcion.get() == 2:
            #Hago un select para saber si ya existe la categoria de "segundos"
            cursor.execute("SELECT * FROM categoria WHERE id == 2")
            resul=cursor.fetchone()
            
            #Si no existe, establezco la categoría. Si existe muestro mensaje de aviso
            if resul == None:
                nomcategoria = [("Segundos")]
            else:
                messagebox.showinfo(title="Alerta",message="Ya existe la categoría para segundos platos") 

        if self.opcion.get() == 3:
            #Hago un select para saber si ya existe la categoria de "postres"
            cursor.execute("SELECT * FROM categoria WHERE id == 3")
            resul = cursor.fetchone()

            #Si no existe, establezco la categoría. Si existe muestro mensaje de aviso
            if resul == None:
                nomcategoria = [("Postres")]
            else:
                messagebox.showinfo(title="Alerta",message="Ya existe la categoría para postres")

        if nomcategoria != "" and resul == None:
            try:
                connection =sqlite3.connect("restaurante.db")
                cursor = connection.cursor()
                cursor.execute("INSERT INTO categoria VALUES(null,?)",nomcategoria) 
            except:
                connection.rollback()
            else:
                messagebox.showinfo("Aviso","La categoría se ha creado correctamente")
                connection.commit()

        #Cierro la conexión a BBDD
        cursor.close() 

    def create_widgets(self):
    	
        #Muestro label informatico
    	self.maintitle = Label(self.master,text="Agregar Categoría", font=("Verdana",12), bg="lightgreen", relief="groove", bd=2).pack()

        #Creo un frame
    	self.frame = Frame(self.master)
    	self.frame.pack(side="left", fill="x")

        #Creo una variable que almacenará el valor de los Radiobutton
    	self.opcion = IntVar()

        #Creo un Radiobutton por cada categoría
    	Radiobutton(self.frame,text="Primeros", variable=self.opcion, value=1).pack(anchor="w")
    	Radiobutton(self.frame,text="Segundos", variable=self.opcion, value=2).pack(anchor="w")
    	Radiobutton(self.frame,text="Postres", variable=self.opcion, value=3).pack(anchor="w")

        #Botón para realizar la acción
    	Button(root,text="Agregar", command=self.agregar_categoria).pack(anchor="center")

root = Tk()
app = Application(root)
app.mainloop()