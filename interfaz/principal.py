import html
import json
import tkinter as tk

from PIL import Image, ImageTk
import requests
import io

import api.api as api

from interfaz.configuracion import IUConfiguracion
from interfaz.constantes import RUTA_CONFIGURACION, RUTA_YOUTUBE


class IUPrincipal:
    def __init__(self, raiz):
        raiz.title("YT-DL")
        raiz.iconbitmap(RUTA_YOUTUBE)
        raiz.resizable(False, False)
        tk.Frame(raiz).grid(column=0, row=0)
        self.raiz = raiz

        self.var_busqueda = tk.StringVar()
        self.entrada_busqueda = tk.Entry(
            raiz, text="Busqueda", textvariable=self.var_busqueda, width=75
        )
        self.entrada_busqueda.grid(column=0, row=0, sticky="NSEW", padx=5, pady=7)

        self.boton_buscar = tk.Button(
            raiz, text="Buscar", command=self.buscar, width=12, pady=0
        )
        self.boton_configurar = tk.Button(
            raiz, text="Configuracion", command=self.configurar, width=12, pady=0
        )
        self.boton_descargar = tk.Button(
            raiz, text="Descargar", command=self.descargar, width=12, pady=0
        )

        self.boton_buscar.grid(column=1, row=0, sticky="NSEW", padx=5, pady=7)
        self.boton_configurar.grid(column=2, row=0, sticky="NSEW", padx=5, pady=7)
        self.boton_descargar.grid(column=2, row=1, sticky="NSEW", padx=5, pady=7)

        self.lista_resultados = tk.Listbox(raiz)
        self.lista_resultados.grid(
            column=0, row=1, columnspan=2, sticky="NSEW", padx=5, pady=7
        )
        self.lista_resultados.bind("<<ListboxSelect>>", self.seleccion)

        self.seleccion(None)

    def buscar(self):
        with open(RUTA_CONFIGURACION, "r") as archivo:
            clave = json.load(archivo)["clave"]

        consulta = self.var_busqueda.get()
        if not consulta:
            return

        respuesta = api.buscar(consulta, clave)
        if respuesta == api.ERROR:
            tk.messagebox.showerror(message="La clave es invalida", title="Clave")
            return
        self.info_resultados = respuesta

        for titulo in list(self.info_resultados.keys()):
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

        api.descargar_video(id, destino)

        tk.messagebox.showinfo(
            message="El video se descargo correctamente", title="Descarga"
        )

    def configurar(self):
        self.configuracion = IUConfiguracion(tk.Toplevel())

    def seleccion(self, evento):
        seleccion = self.lista_resultados.curselection()
        if not seleccion:
            return

        self.descripcion = tk.Frame(self.raiz)
        self.descripcion.grid(column=0, row=2, columnspan=3)

        titulo = self.lista_resultados.get(seleccion[0])
        canal = self.info_resultados[titulo]["canal"]
        fecha = self.info_resultados[titulo]["fecha"][:10]
        descripcion = self.info_resultados[titulo]["descripcion"]
        formato = f"{titulo}\n\n{canal}\n\n{fecha}\n\n{descripcion}"

        self.descripcion_texto = tk.Text(
            self.descripcion, height=10, width=50, wrap=tk.WORD
        )
        self.descripcion_texto.grid(column=1, row=0, sticky="NSEW", padx=5, pady=5)

        self.descripcion_texto.delete(1.0, tk.END)
        self.descripcion_texto.insert(tk.INSERT, formato)
        self.descripcion_texto.config(state=tk.DISABLED)

        url = self.info_resultados[titulo]["miniatura"]
        data = requests.get(url).content
        img = Image.open(io.BytesIO(data)).resize((240, 180))
        self.miniatura = ImageTk.PhotoImage(img)

        self.etiqueta_imagen = tk.Label(self.descripcion, image=self.miniatura)
        self.etiqueta_imagen.grid(column=0, row=0, sticky="NSEW", padx=5, pady=5)
