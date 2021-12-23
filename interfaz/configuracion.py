import json
import tkinter as tk
from tkinter import filedialog

from interfaz.constantes import RUTA_CONFIGURACION, RUTA_ENGRANAJE


class IUConfiguracion:
    def __init__(self, raiz):
        raiz.title("Configuracion")
        raiz.iconbitmap(RUTA_ENGRANAJE)
        tk.Frame(raiz).grid(column=0, row=0)
        self.raiz = raiz

        self.etiqueta_clave = tk.Label(raiz, text="Clave del API: ", anchor="w")
        self.etiqueta_carpeta = tk.Label(raiz, text="Carpeta de Descarga: ", anchor="w")

        self.etiqueta_clave.grid(column=0, row=0, sticky="NSEW", padx=5, pady=5)
        self.etiqueta_carpeta.grid(column=0, row=1, sticky="NSEW", padx=5, pady=5)

        self.var_clave = tk.StringVar()
        self.var_carpeta = tk.StringVar()
        self.entrada_clave = tk.Entry(raiz, textvariable=self.var_clave, width=55)
        self.entrada_carpeta = tk.Entry(raiz, textvariable=self.var_carpeta, width=43)

        self.entrada_clave.grid(
            column=1, row=0, columnspan=2, sticky="EW", padx=5, pady=5
        )
        self.entrada_carpeta.grid(column=1, row=1, sticky="EW", padx=5, pady=5)

        self.boton_navegar = tk.Button(
            raiz, text="...", command=self.navegar, width=9, pady=0
        )
        self.boton_guardar = tk.Button(
            raiz, text="Guardar", command=self.guardar, width=9, pady=0
        )

        self.boton_navegar.grid(column=2, row=1, sticky="NSEW", padx=5, pady=5)
        self.boton_guardar.grid(column=2, row=2, sticky="NSEW", padx=5, pady=5)

        self.obtener_configuracion()

    def obtener_configuracion(self):
        with open(RUTA_CONFIGURACION, "r") as archivo:
            configuracion = json.load(archivo)
            carpeta = configuracion["carpeta"]
            clave = configuracion["clave"]

        self.var_clave.set(clave)
        self.var_carpeta.set(carpeta)

    def guardar(self):
        data = {"clave": self.var_clave.get(), "carpeta": self.var_carpeta.get()}
        with open(RUTA_CONFIGURACION, "w") as archivo:
            json.dump(data, archivo)
        self.raiz.destroy()

    def navegar(self):
        self.var_carpeta.set(filedialog.askdirectory())


if __name__ == "__main__":
    root = tk.Tk()
    principal = IUConfiguracion(root)
    root.mainloop()
