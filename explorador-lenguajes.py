import tkinter as tk
from tkinter import ttk
from tkinter import ttk, messagebox

def validar_alfabeto(texto):
    elementos = texto.split(",")
    simbolos = []

    for elemento in elementos:
        simbolo = elemento.strip()

        if simbolo == "":
            return [], "El alfabeto no puede tener elementos vacíos."

        if simbolo == "ε":
            return [], "ε representa la cadena vacía y no es un símbolo."

        if len(simbolo) != 1:
            return [], "Escribe un solo carácter por símbolo."

        if simbolo in simbolos:
            return [], "El símbolo '" + simbolo + "' está repetido."

        simbolos.append(simbolo)

    return simbolos, ""

def representar_alfabeto(simbolos):
    texto = "{"
    cantidad = 0

    for simbolo in simbolos:
        if cantidad > 0:
            texto = texto + ", "

        texto = texto + simbolo
        cantidad = cantidad + 1

    texto = texto + "}"

    return texto, cantidad

def main():
    ventana = tk.Tk()
    ventana.title("Explorador de alfabetos, cadenas y lenguejes")
    ventana.geometry("900x600")
    ventana.minsize(750, 500)
    alfabeto = []

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

    instrucciones = ttk.Label(
    panel_alfabeto,
    text="Escribe los símbolos separados por comas. Ejemplo: a,b,c"
    )
    instrucciones.pack(anchor="w", pady=(0, 10))

    entrada_alfabeto = ttk.Entry(
        panel_alfabeto,
        width=50
    )
    entrada_alfabeto.pack(anchor="w", fill="x", pady=(0, 10))

    nota = ttk.Label(
        panel_alfabeto,
        text=(
            "Cada símbolo debe tener un carácter. "
            "No se permiten símbolos repetidos ni ε."
        ),
        wraplength=650
    )
    nota.pack(anchor="w", pady=(0, 15))

    resultado_alfabeto = tk.StringVar(
        value="Todavía no has guardado un alfabeto."
    )

    def guardar_alfabeto():
        texto = entrada_alfabeto.get()
        nuevos_simbolos, error = validar_alfabeto(texto)

        if error != "":
            messagebox.showerror(
                "Alfabeto inválido",
                error,
                parent=ventana
            )
            return

        alfabeto.clear()

        for simbolo in nuevos_simbolos:
            alfabeto.append(simbolo)

        conjunto, cardinalidad = representar_alfabeto(alfabeto)

        estado_alfabeto.set("Alfabeto actual: Σ = " + conjunto)

        resultado_alfabeto.set(
            "Σ = " + conjunto
            + "\n|Σ| = " + str(cardinalidad)
            + "\n\nAlfabeto guardado correctamente."
        )

    boton_guardar = ttk.Button(
        panel_alfabeto,
        text="Guardar / cambiar alfabeto",
        command=guardar_alfabeto
    )
    boton_guardar.pack(anchor="w", pady=(0, 20))

    etiqueta_resultado = ttk.Label(
        panel_alfabeto,
        textvariable=resultado_alfabeto,
        wraplength=650,
        justify="left"
    )
    etiqueta_resultado.pack(anchor="w")

    entrada_alfabeto.focus_set()

    ventana.mainloop()

if __name__ == "__main__":
    main()

