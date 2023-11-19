import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
import pygame
import pickle
import os
from functools import partial

class BotoneraEfectosSonido:
    def __init__(self, root):
        self.root = root
        self.root.title("Botonera")

        # Configurar la ventana para que no se pueda maximizar
        self.root.resizable(width=True, height=True)
        self.root.maxsize(width=self.root.winfo_screenwidth(), height=self.root.winfo_screenheight())

        # Ocultar la ventana principal antes de mostrar la advertencia
        self.root.iconify()

        # Mostrar un mensaje de advertencia al abrir el programa
        messagebox.showinfo("Botonera | AD Soft", "⚠|Es recomendable guardar los efectos en la carpeta 'Sonidos' para no moverlos de lugar y evitar fallas del programa.")

        # Volver a mostrar la ventana principal después de cerrar la advertencia
        self.root.deiconify()

        self.efectos_sonido = self.cargar_configuracion()

        self.boton_mas = tk.Button(self.root, text="+", font=("Arial", 24), command=self.agregar_efecto)
        self.boton_mas.grid(row=0, column=0)

        self.actualizar_botones()

        # Configurar el evento de cierre de la ventana principal
        self.root.protocol("WM_DELETE_WINDOW", self.cerrar_programa)

    def cargar_configuracion(self):
        if os.path.exists("configBotones.pkl"):
            with open("configBotones.pkl", "rb") as archivo_config:
                return pickle.load(archivo_config)
        return []

    def guardar_configuracion(self):
        with open("configBotones.pkl", "wb") as archivo_config:
            pickle.dump(self.efectos_sonido, archivo_config)

    def agregar_efecto(self):
        nombre_efecto = simpledialog.askstring("Nombre", "Ingrese el nombre del efecto:")
        if nombre_efecto:
            archivo_audio = filedialog.askopenfilename(title="Seleccionar archivo de audio", filetypes=[("Archivos de audio", "*.mp3;*.wav")])
            if archivo_audio:
                self.efectos_sonido.append({"nombre": nombre_efecto, "audio": archivo_audio})
                self.actualizar_botones()
                self.guardar_configuracion()

    def eliminar_efecto(self, efecto):
        self.efectos_sonido.remove(efecto)
        self.actualizar_botones()
        self.guardar_configuracion()

    def reproducir_efecto(self, efecto):
        pygame.mixer.init()
        pygame.mixer.music.load(efecto["audio"])
        pygame.mixer.music.play()

    def mostrar_menu_contextual(self, event, efecto):
        menu = tk.Menu(self.root, tearoff=0)
        menu.add_command(label="Eliminar", command=partial(self.eliminar_efecto, efecto))
        menu.post(event.x_root, event.y_root)

    def cerrar_programa(self):
        # Verificar si hay música en reproducción antes de detenerla
        if pygame.mixer.get_busy():
            pygame.mixer.music.stop()

        # Guardar configuración
        self.guardar_configuracion()

        # Cerrar la ventana principal
        self.root.destroy()

    def actualizar_botones(self):
        # Limpiamos la interfaz antes de actualizarla
        for widget in self.root.winfo_children():
            if widget != self.boton_mas:
                widget.destroy()

        # Calculamos el tamaño de la cuadrícula
        num_efectos = len(self.efectos_sonido)
        num_columnas = 3
        num_filas = -(-num_efectos // num_columnas)  # Redondeo hacia arriba

        # Creamos los botones
        for i, efecto in enumerate(self.efectos_sonido):
            row = i // num_columnas + 1
            col = i % num_columnas
            boton = tk.Button(self.root, text=efecto["nombre"], font=("Arial", 12), command=partial(self.reproducir_efecto, efecto))
            boton.grid(row=row, column=col)
            boton.bind("<Button-3>", lambda event, e=efecto: self.mostrar_menu_contextual(event, e))

        # Colocamos el botón "+" en la posición siguiente
        row = num_filas + 1
        col = num_efectos % num_columnas
        self.boton_mas.grid(row=row, column=col)

if __name__ == "__main__":
    root = tk.Tk()
    app = BotoneraEfectosSonido(root)

    # Configurar la ventana como siempre en la parte superior
    root.wm_attributes("-topmost", 1)
    root.mainloop()
