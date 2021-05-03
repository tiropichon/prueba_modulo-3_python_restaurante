from tkinter import *
from tkinter import messagebox
import sqlite3

class Application(Frame):
	def __init__(self, master=None):
		super().__init__(master=None)
		self.master = master
		self.master.title("Agregar plato...")
		self.crear_bd()
		self.crear_widget()

	def crear_bd(self):
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

	def agregar_plato(self):
		correcto = False
		connection = sqlite3.connect("restaurante.db")
		cursor = connection.cursor()
		cursor.execute("SELECT * FROM categoria")
		categorias = cursor.fetchall()

		for categoria in categorias:
			if categoria[0] == self.opcion.get():
				correcto = False

		while correcto == False:
			nomplato = self.nomplato.get()
			if nomplato == "":
				correcto = True
				connection.rollback()
				messagebox.showinfo("Aviso", "Debe introducir un nombre de plato y/o seleccionar una categoria")
			else:
				plato=[(self.nomplato.get()),(self.opcion.get())]
				try:
					cursor.execute("INSERT INTO plato VALUES(null,?,?)",plato)
					connection.commit()
				except:
					messagebox.showinfo("Aviso","Ese nombre de plato ya existe")
					break
				else:
					correcto = True
					messagebox.showinfo("Aviso","Plato insertado correctamente")
					self.nomplato.delete(0,END)
					self.opcion.set(0)
		cursor.close()

	def crear_widget(self):
		self.maintitle = Label(self.master,text="Agregar Plato", font=("Verdana",12), bg="lightgreen", relief="groove", bd=2).pack()
		self.frame = Frame(self.master)
		self.frame.pack(side="left")
		
		self.opcion = IntVar()
		self.nomplato = StringVar()

		Label(self.frame,text="Seleccione categoría:").pack()
		Radiobutton(self.frame,text="Primeros", variable=self.opcion, value=1).pack(anchor="w")
		Radiobutton(self.frame,text="Segundos", variable=self.opcion, value=2).pack(anchor="w")
		Radiobutton(self.frame,text="Postres", variable=self.opcion, value=3).pack(anchor="w")
		Label(self.frame,text="").pack()
		Label(self.frame,text="Introduzca el plato:").pack()
		self.nomplato = Entry(self.frame)
		self.nomplato.pack()
		self.boton = Button(self.frame, text="Agregar", command=self.agregar_plato).pack()
		pass


root = Tk()
app = Application(root)
app.mainloop()