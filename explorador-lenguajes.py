import tkinter as tk
from tkinter import ttk

def main():
    ventana = tk.Tk()
    ventana.title("Explorador de alfabetos, cadenas y lenguejes")
    ventana.geometry("900x600")
    ventana.minsize(750, 500)

    titulo = ttk.Label(
        ventana,
        text = "Explorador de alfabetos, cadenas y lenguajes",
        font = ("Arial", 18, "bold")
    )
    titulo.pack(pady=(20, 10))

    estado_alfabeto = tk.StringVar(value="Alfabeto actual: sin definir")

    etiqueta_alfabeto = ttk.Label(
        ventana,
        textvariable = estado_alfabeto
    )
    etiqueta_alfabeto.pack(pady=(0, 15))

    pestanas = ttk.Notebook(ventana)
    pestanas.pack(fill="both", expand=True, padx=20, pady=(0, 20))

    panel_alfabeto = ttk.Frame(pestanas, padding=20)
    panel_cadenas = ttk.Frame(pestanas, padding=20)
    panel_generacion = ttk.Frame(pestanas, padding=20)
    panel_lenguajes = ttk.Frame(pestanas, padding=20)
    panel_chomsky = ttk.Frame(pestanas, padding=20)

    pestanas.add(panel_alfabeto, text="Alfabeto")
    pestanas.add(panel_cadenas, text="Cadenas")
    pestanas.add(panel_generacion, text="Generación")
    pestanas.add(panel_lenguajes, text="Lenguajes finitos")
    pestanas.add(panel_chomsky, text="Jerarquía de Chomsky")

    ventana.mainloop()

if __name__ == "__main__":
    main()

