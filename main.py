from coches import Coches
from tkinter import Tk, Label, Entry, Button, messagebox


class App:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Gestion de coches")
        self.ventana.geometry("400x700")
        self.ventana.resizable(0, 0)
        self.lista_coches = []   # aquí se guardan los coches (simula la BD)
        self.indice = None       # posición del coche que se está modificando
        self.entradas = {}
        self.id_entry = None
        self.main()

    # ---------- utilidades ----------
    def borrarPantalla(self):
        for widget in self.ventana.winfo_children():
            widget.destroy()

    def respuesta_sql(self, respuesta):
        if respuesta:
            messagebox.showinfo(title="::EXITO::", message="Accion realizada con exito")
        else:
            messagebox.showerror(title="VERIFIQUE", message="Esta accion no pudo realizarse con exito")

    def reiniciar(self):
        """Limpia el estado temporal y regresa al menú de coches."""
        self.indice = None
        self.entradas = {}
        self.id_entry = None
        self.menuAcciones()

    # ---------- menús ----------
    def main(self):
        self.borrarPantalla()
        Label(self.ventana, text="::: MENU PRINCIPAL :::").pack(pady=20)
        Button(self.ventana, text="1.- Coches", command=self.menuAcciones).pack(pady=10)
        Button(self.ventana, text="2.- Salir", command=self.ventana.quit).pack(pady=10)

    def menuAcciones(self):
        self.borrarPantalla()
        Label(self.ventana, text=":::: Menu de Coches ::::").pack(pady=10)
        Button(self.ventana, text="1.- Agregar", command=self.insertar_coche_view).pack(pady=10)
        Button(self.ventana, text="2.- Borrar", command=self.borrar_coche_view).pack(pady=10)
        Button(self.ventana, text="3.- Modificar", command=self.pedir_id_view).pack(pady=10)
        Button(self.ventana, text="4.- Mostrar", command=self.consultar_coche_view).pack(pady=10)
        Button(self.ventana, text="5.- Salir", command=self.main).pack(pady=10)

    # ---------- formulario reutilizable (agregar y modificar) ----------
    def formulario(self, titulo, texto_boton, comando, coche=None):
        self.borrarPantalla()
        Label(self.ventana, text=titulo).pack(pady=10)
        campos = [("Marca", "marca"), ("Color", "color"), ("Modelo", "modelo"),
                  ("Velocidad", "velocidad_maxima"), ("Potencia", "potencia"),
                  ("Asientos", "asientos")]
        self.entradas = {}
        for etiqueta, atributo in campos:
            Label(self.ventana, text=etiqueta).pack(pady=5)
            entrada = Entry(self.ventana)
            entrada.pack(pady=3)
            if coche:  # al modificar, se rellena con los datos actuales
                entrada.insert(0, str(getattr(coche, atributo)))
            self.entradas[atributo] = entrada
        self.entradas["marca"].focus()
        Button(self.ventana, text=texto_boton, command=comando).pack(pady=10)
        Button(self.ventana, text="::Regresar::", command=self.reiniciar).pack(pady=5)

    def leer_formulario(self):
        """Lee los campos y crea un Coches. Lanza ValueError si algo es inválido."""
        e = self.entradas
        marca = e["marca"].get().strip()
        color = e["color"].get().strip()
        modelo = e["modelo"].get().strip()
        if not marca or not color or not modelo:
            raise ValueError("Campos de texto vacios")
        # orden de la clase: color, marca, modelo, velocidad_maxima, potencia, asientos
        return Coches(color, marca, modelo,
                      int(e["velocidad_maxima"].get()),
                      int(e["potencia"].get()),
                      int(e["asientos"].get()))

    # ---------- AGREGAR ----------
    def insertar_coche_view(self):
        self.formulario("Ingresar datos del Coche", "Agregar", self.insertar_coche_controller)

    def insertar_coche_controller(self):
        try:
            self.lista_coches.append(self.leer_formulario())
            self.respuesta_sql(True)
            self.reiniciar()
        except ValueError:
            self.respuesta_sql(False)

    # ---------- MOSTRAR ----------
    def consultar(self):
        # Simula las filas de la BD: (id, color, modelo, vel_max, marca, potencia, asientos)
        registros = []
        for i, c in enumerate(self.lista_coches, start=1):
            registros.append((i, c.color, c.modelo, c.velocidad_maxima,
                              c.marca, c.potencia, c.asientos))
        return registros

    def consultar_coche_controller(self):
        registros = self.consultar()
        if not registros:
            return "No hay coches registrados"
        filas = ""
        for fila in registros:
            filas += (f"\nID: {fila[0]}"
                      f"\nMarca: {fila[4]}   Modelo: {fila[2]}   Color: {fila[1]}"
                      f"\nVelocidad: {fila[3]} km/h   Potencia: {fila[5]} HP"
                      f"   Asientos: {fila[6]}\n")
        return filas

    def consultar_coche_view(self):
        self.borrarPantalla()
        Label(self.ventana, text="..:: Consultar Coches ::..").pack(pady=10)
        Label(self.ventana, text=self.consultar_coche_controller(),
              justify="left").pack(pady=10)
        Button(self.ventana, text="::Regresar::", command=self.reiniciar).pack(pady=10)

    # ---------- BORRAR ----------
    def borrar_coche_view(self):
        self.borrarPantalla()
        Label(self.ventana, text="..:: Borrar Coche ::..").pack(pady=10)
        Label(self.ventana, text=self.consultar_coche_controller(),
              justify="left").pack(pady=10)
        Label(self.ventana, text="ID del coche a borrar").pack(pady=5)
        self.id_entry = Entry(self.ventana)
        self.id_entry.focus()
        self.id_entry.pack(pady=5)
        Button(self.ventana, text="Borrar", command=self.borrar_coche_controller).pack(pady=10)
        Button(self.ventana, text="::Regresar::", command=self.reiniciar).pack(pady=5)

    def borrar_coche_controller(self):
        try:
            pos = int(self.id_entry.get()) - 1
            if not 0 <= pos < len(self.lista_coches):
                raise ValueError
            self.lista_coches.pop(pos)
            self.respuesta_sql(True)
            self.borrar_coche_view()   # refresca la lista
        except ValueError:
            self.respuesta_sql(False)

    # ---------- MODIFICAR ----------
    def pedir_id_view(self):
        self.borrarPantalla()
        Label(self.ventana, text="..:: Modificar Coche ::..").pack(pady=10)
        Label(self.ventana, text=self.consultar_coche_controller(),
              justify="left").pack(pady=10)
        Label(self.ventana, text="ID del coche a modificar").pack(pady=5)
        self.id_entry = Entry(self.ventana)
        self.id_entry.focus()
        self.id_entry.pack(pady=5)
        Button(self.ventana, text="Buscar", command=self.modificar_coche_view).pack(pady=10)
        Button(self.ventana, text="::Regresar::", command=self.reiniciar).pack(pady=5)

    def modificar_coche_view(self):
        try:
            pos = int(self.id_entry.get()) - 1
            if not 0 <= pos < len(self.lista_coches):
                raise ValueError
        except ValueError:
            self.respuesta_sql(False)
            return
        self.indice = pos
        self.formulario("Modificar datos del Coche", "Guardar cambios",
                        self.modificar_coche_controller, self.lista_coches[pos])

    def modificar_coche_controller(self):
        try:
            self.lista_coches[self.indice] = self.leer_formulario()
            self.respuesta_sql(True)
            self.reiniciar()
        except ValueError:
            self.respuesta_sql(False)


if __name__ == "__main__":
    ventana = Tk()
    app = App(ventana)
    ventana.mainloop()