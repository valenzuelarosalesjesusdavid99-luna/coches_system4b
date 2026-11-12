from tkinter import Tk, Frame, Label, Entry, Button, messagebox, ttk
from coches import Coches

# (texto de la etiqueta, atributo de la clase Coches)
CAMPOS = [("Marca", "marca"), ("Color", "color"), ("Modelo", "modelo"),
          ("Velocidad", "velocidad_maxima"), ("Potencia", "potencia"),
          ("Asientos", "asientos")]


class App:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Gestion de coches")
        self.ventana.geometry("520x600")
        self.ventana.resizable(0, 0)
        self.lista_coches = []
        self.indice = None
        self.entradas = {}
        self.contenedor = Frame(self.ventana)
        self.contenedor.pack(fill="both", expand=True)
        self.menu_principal()

    # ---------- utilidades ----------
    def limpiar(self):
        """Destruye los widgets Y reinicia el estado temporal."""
        for w in self.contenedor.winfo_children():
            w.destroy()
        self.indice = None
        self.entradas = {}

    def aviso(self, ok):
        if ok:
            messagebox.showinfo("::EXITO::", "Accion realizada con exito")
        else:
            messagebox.showerror("VERIFIQUE", "Esta accion no pudo realizarse con exito")

    def boton(self, texto, comando):
        Button(self.contenedor, text=texto, command=comando, width=20).pack(pady=6)

    def tabla(self):
        """Crea una tabla con los coches y la regresa."""
        cols = ("id", "marca", "modelo", "color", "vel", "pot", "asientos")
        tv = ttk.Treeview(self.contenedor, columns=cols, show="headings", height=8)
        for c in cols:
            tv.heading(c, text=c.capitalize())
            tv.column(c, width=65, anchor="center")
        for i, c in enumerate(self.lista_coches):
            # iid = posición en la lista, así sabemos cuál se seleccionó
            tv.insert("", "end", iid=str(i),
                      values=(i + 1, c.marca, c.modelo, c.color,
                              c.velocidad_maxima, c.potencia, c.asientos))
        tv.pack(pady=10)
        return tv

    def seleccionado(self, tv):
        """Regresa la posición del coche elegido, o None si no hay selección."""
        sel = tv.selection()
        return int(sel[0]) if sel else None

    # ---------- menús ----------
    def menu_principal(self):
        self.limpiar()
        Label(self.contenedor, text="::: MENU PRINCIPAL :::").pack(pady=20)
        self.boton("1.- Coches", self.menu_coches)
        self.boton("2.- Salir", self.ventana.quit)

    def menu_coches(self):
        self.limpiar()
        Label(self.contenedor, text=":::: Menu de Coches ::::").pack(pady=10)
        self.boton("1.- Agregar", self.agregar_view)
        self.boton("2.- Borrar", self.borrar_view)
        self.boton("3.- Modificar", self.modificar_view)
        self.boton("4.- Mostrar", self.mostrar_view)
        self.boton("5.- Salir", self.menu_principal)

    # ---------- formulario reutilizable ----------
    def formulario(self, titulo, texto_boton, comando, coche=None):
        self.limpiar()
        Label(self.contenedor, text=titulo).pack(pady=10)
        for etiqueta, atributo in CAMPOS:
            Label(self.contenedor, text=etiqueta).pack(pady=3)
            entrada = Entry(self.contenedor)
            entrada.pack()
            if coche:
                entrada.insert(0, str(getattr(coche, atributo)))
            self.entradas[atributo] = entrada
        self.entradas["marca"].focus()
        self.boton(texto_boton, comando)
        self.boton("::Regresar::", self.menu_coches)

    def leer_formulario(self):
        e = self.entradas
        marca = e["marca"].get().strip()
        color = e["color"].get().strip()
        modelo = e["modelo"].get().strip()
        if not marca or not color or not modelo:
            raise ValueError("Campos vacios")
        return Coches(color, marca, modelo,
                      int(e["velocidad_maxima"].get()),
                      int(e["potencia"].get()),
                      int(e["asientos"].get()))

    # ---------- AGREGAR ----------
    def agregar_view(self):
        self.formulario("Ingresar datos del Coche", "Agregar", self.agregar_controller)

    def agregar_controller(self):
        try:
            self.lista_coches.append(self.leer_formulario())
            self.aviso(True)
            self.menu_coches()
        except ValueError:
            self.aviso(False)

    # ---------- MOSTRAR ----------
    def mostrar_view(self):
        self.limpiar()
        Label(self.contenedor, text="..:: Consultar Coches ::..").pack(pady=10)
        self.tabla()
        self.boton("::Regresar::", self.menu_coches)

    # ---------- BORRAR ----------
    def borrar_view(self):
        self.limpiar()
        Label(self.contenedor, text="..:: Borrar Coche ::.. (selecciona uno)").pack(pady=10)
        tv = self.tabla()
        self.boton("Borrar", lambda: self.borrar_controller(tv))
        self.boton("::Regresar::", self.menu_coches)

    def borrar_controller(self, tv):
        pos = self.seleccionado(tv)
        if pos is None:
            self.aviso(False)
            return
        self.lista_coches.pop(pos)
        self.aviso(True)
        self.borrar_view()  # refresca la tabla

    # ---------- MODIFICAR ----------
    def modificar_view(self):
        self.limpiar()
        Label(self.contenedor, text="..:: Modificar Coche ::.. (selecciona uno)").pack(pady=10)
        tv = self.tabla()
        self.boton("Modificar", lambda: self.modificar_form(tv))
        self.boton("::Regresar::", self.menu_coches)

    def modificar_form(self, tv):
        pos = self.seleccionado(tv)
        if pos is None:
            self.aviso(False)
            return
        coche = self.lista_coches[pos]
        self.formulario("Modificar datos del Coche", "Guardar cambios",
                        self.modificar_controller, coche)
        self.indice = pos  # se asigna DESPUÉS de formulario() porque limpiar() lo pone en None

    def modificar_controller(self):
        try:
            self.lista_coches[self.indice] = self.leer_formulario()
            self.aviso(True)
            self.menu_coches()
        except ValueError:
            self.aviso(False)


if __name__ == "__main__":
    ventana = Tk()
    App(ventana)
    ventana.mainloop()