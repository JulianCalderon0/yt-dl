import os
import tkinter as tk

from interfaz.principal import IUPrincipal

if __name__ == "__main__":
    cwd = os.path.dirname(os.path.realpath(__file__))
    os.chdir(cwd)

    root = tk.Tk()
    principal = IUPrincipal(root)
    root.mainloop()
