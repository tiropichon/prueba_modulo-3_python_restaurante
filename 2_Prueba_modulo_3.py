'''En este ejercicios debes crear una interfaz gráfica con tkinter (menu.py) que muestre de forma elegante 
el menú del restaurante.

Tú eliges el nombre del restaurante y el precio del menú, así como las tipografías, colores, adornos y tamaño 
de la ventana.

El único requisito es que el programa se conectará a la base de datos para buscar la lista categorías y platos.
'''
# -*- coding: utf-8 -*-
from tkinter import *
import sqlite3

def crear_bd():
	connection = sqlite3.connect("restaurante.db")
	cursor = connection.cursor()

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


class Application(Frame):
    def __init__(self, master=None):
    	super().__init__(master=None)
    	self.master = master
    	self.master.title("Carta del Restaurante")
    	self.master.geometry('460x240')
    	self.master.resizable(0,0)
    	self.master.config(bg="pink")
    	crear_bd()
    	self.create_widgets()

    def mostrar_menu(self):
    	connection = sqlite3.connect("restaurante.db") 
    	cursor = connection.cursor()
    	cursor.execute("SELECT * FROM plato ORDER BY categoria_id")
    	platos = cursor.fetchall()

    	texto = ""
    	texto2 = ""
    	texto3 = ""

    	for plato in platos:
    		if plato[2] == 1:
    			texto += "-> "+plato[1]+"\n"

    		if plato[2] == 2:
    			texto2 += "-> "+plato[1]+"\n"

    		if plato[2] == 3:
    			texto3 += "-> "+plato[1]+"\n"
    			 
    	self.textoPrimeros.insert(INSERT,texto)
    	self.textoSegundos.insert(INSERT,texto2)
    	self.textoPostres.insert(INSERT,texto3)

    def create_widgets(self):
    	self.opcPrimeros = IntVar()
    	self.opcSegundos = IntVar()
    	self.opcPostres = IntVar()
    	
    	self.maintitle = Label(self.master,text="Menu del restaurante", font=("Verdana",24), bg="lightgreen", fg="red").grid(row=0,column=0, columnspan=3)
    	Label(root, bg="pink").grid(row=1, column=0, columnspan=3)

    	self.primerostitle = Label(self.master,text="Primeros",font=("Verdana",12), bg="red").grid(row=2,column=0)
    	Label(root, bg="pink").grid(row=3, column=0, columnspan=3)
    	self.textoPrimeros = Text(self.master, width=25, height=10, font=("Tahoma",8), bg="lightblue")
    	self.textoPrimeros.grid(row=4, column=0)

    	self.segundostitle = Label(self.master,text="Segundos",font=("Verdana",12), bg="red").grid(row=2,column=1)
    	Label(root, bg="pink").grid(row=3, column=0, columnspan=3)
    	self.textoSegundos = Text(self.master, width=25, height=10, font=("Tahoma",8), bg="lightblue")
    	self.textoSegundos.grid(row=4, column=1)

    	self.postrestitle = Label(self.master,text="Postres",font=("Verdana",12), bg="red").grid(row=2,column=2)
    	Label(root, bg="pink").grid(row=3, column=0, columnspan=3)
    	self.textoPostres = Text(self.master, width=25, height=10, font=("Tahoma",8), bg="lightblue")
    	self.textoPostres.grid(row=4, column=2)

    	self.mostrar_menu()

root = Tk()
app = Application(root)
app.mainloop()