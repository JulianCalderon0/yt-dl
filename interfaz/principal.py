import html
import json
import tkinter as tk

import api.api as api

from interfaz.configuracion import IUConfiguracion
from interfaz.constantes import RUTA_CONFIGURACION, RUTA_YOUTUBE

TITULO_PRINCIPAL = "YT-DL"


class IUPrincipal:
    def __init__(self, raiz):
        raiz.title(TITULO_PRINCIPAL)
        raiz.iconbitmap(RUTA_YOUTUBE)
        tk.Frame(raiz).grid(column=0, row=0)
        self.raiz = raiz

        self.var_busqueda = tk.StringVar()
        self.entrada_busqueda = tk.Entry(
            raiz, text="Busqueda", textvariable=self.var_busqueda, width=75
        )
        self.entrada_busqueda.grid(column=0, row=0, sticky="NSEW", padx=5, pady=7)

        self.boton_buscar = tk.Button(
            raiz, text="Buscar", command=self.buscar, width=12
        )
        self.boton_configurar = tk.Button(
            raiz, text="Configuracion", command=self.configurar, width=12
        )
        self.boton_descargar = tk.Button(
            raiz, text="Descargar", command=self.descargar, width=12
        )

        self.boton_buscar.grid(column=1, row=0, sticky="NSEW", padx=5, pady=7)
        self.boton_configurar.grid(column=2, row=0, sticky="NSEW", padx=5, pady=7)
        self.boton_descargar.grid(column=2, row=1, sticky="NSEW", padx=5, pady=7)

        self.lista_resultados = tk.Listbox(raiz)
        self.lista_resultados.grid(
            column=0, row=1, columnspan=2, sticky="NSEW", padx=5, pady=7
        )

    def buscar(self):
        with open(RUTA_CONFIGURACION, "r") as archivo:
            clave = json.load(archivo)["clave"]

        consulta = self.var_busqueda.get()
        if not consulta:
            return

        self.info_resultados = api.buscar(consulta, clave)
        if self.info_resultados == api.ERROR:
            return

        for titulo in [*self.info_resultados.keys()]:
            f_titulo = html.unescape(titulo)
            self.info_resultados[f_titulo] = self.info_resultados.pop(titulo)

        self.lista_resultados.delete(0, tk.END)
        self.lista_resultados.insert(tk.END, *self.info_resultados.keys())

    def descargar(self):
        seleccion = self.lista_resultados.curselection()
        if not seleccion:
            return

        with open(RUTA_CONFIGURACION, "r") as archivo:
            destino = json.load(archivo)["carpeta"]

        titulo = self.lista_resultados.get(seleccion[0])
        id = self.info_resultados[titulo]["id"]

        self.raiz.title("Descargando")
        api.descargar_video(id, destino)
        self.raiz.title(TITULO_PRINCIPAL)

    def configurar(self):
        self.configuracion = IUConfiguracion(tk.Toplevel())
