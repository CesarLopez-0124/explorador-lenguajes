import tkinter as tk
from tkinter import ttk, messagebox


# Validación y representación del alfabeto

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


# Validación y representación de cadenas

def interpretar_cadena(texto):
    if texto == "ε":
        return ""

    return texto


def mostrar_cadena(cadena):
    if cadena == "":
        return "ε"

    return cadena


def pertenece_al_alfabeto(cadena, alfabeto):
    for simbolo in cadena:
        if simbolo not in alfabeto:
            return False

    return True


# Interfaz gráfica

def main():
    ventana = tk.Tk()
    ventana.title("Explorador de alfabetos, cadenas y lenguajes")
    ventana.geometry("900x600")
    ventana.minsize(750, 500)

    alfabeto = []

    # Variables que muestran información en la interfaz
    estado_alfabeto = tk.StringVar(
        value="Alfabeto actual: sin definir"
    )

    resultado_alfabeto = tk.StringVar(
        value="Todavía no has guardado un alfabeto."
    )

    resultado_cadenas = tk.StringVar(
        value="Introduce las cadenas y pulsa Validar."
    )

    valor_w = tk.StringVar()
    valor_v = tk.StringVar()

    # Encabezado
    titulo = ttk.Label(
        ventana,
        text="Explorador de alfabetos, cadenas y lenguajes",
        font=("Arial", 18, "bold")
    )
    titulo.pack(pady=(20, 10))

    etiqueta_alfabeto = ttk.Label(
        ventana,
        textvariable=estado_alfabeto,
        wraplength=700
    )
    etiqueta_alfabeto.pack(pady=(0, 15))

    # Pestañas
    pestanas = ttk.Notebook(ventana)
    pestanas.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=(0, 20)
    )

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

    # Controles de la pestaña Alfabeto
    instrucciones = ttk.Label(
        panel_alfabeto,
        text="Escribe los símbolos separados por comas. Ejemplo: a,b,c"
    )
    instrucciones.pack(anchor="w", pady=(0, 10))

    entrada_alfabeto = ttk.Entry(
        panel_alfabeto,
        width=50
    )
    entrada_alfabeto.pack(
        anchor="w",
        fill="x",
        pady=(0, 10)
    )

    nota = ttk.Label(
        panel_alfabeto,
        text=(
            "Cada símbolo debe tener un carácter. "
            "No se permiten símbolos repetidos ni ε."
        ),
        wraplength=650
    )
    nota.pack(anchor="w", pady=(0, 15))

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

        # Solo sustituimos el alfabeto cuando la entrada es válida.
        alfabeto.clear()

        for simbolo in nuevos_simbolos:
            alfabeto.append(simbolo)

        conjunto, cardinalidad = representar_alfabeto(alfabeto)

        estado_alfabeto.set(
            "Alfabeto actual: Σ = " + conjunto
        )

        resultado_alfabeto.set(
            "Σ = " + conjunto
            + "\n|Σ| = " + str(cardinalidad)
            + "\n\nAlfabeto guardado correctamente."
        )

        resultado_cadenas.set(
            "Alfabeto actualizado. Vuelve a validar las cadenas."
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

    # Controles de la pestaña Cadenas
    instrucciones_cadenas = ttk.Label(
        panel_cadenas,
        text=(
            "Escribe cadenas usando el alfabeto actual. "
            "Deja un campo vacío o pulsa ε para representar la cadena vacía."
        ),
        wraplength=650
    )
    instrucciones_cadenas.pack(anchor="w", pady=(0, 15))

    # Campo para w
    fila_w = ttk.Frame(panel_cadenas)
    fila_w.pack(fill="x", pady=(0, 10))

    ttk.Label(
        fila_w,
        text="Cadena w:",
        width=12
    ).pack(side="left")

    entrada_w = ttk.Entry(
        fila_w,
        textvariable=valor_w
    )
    entrada_w.pack(
        side="left",
        fill="x",
        expand=True,
        padx=10
    )

    def poner_epsilon_w():
        valor_w.set("ε")
        entrada_w.focus_set()

    ttk.Button(
        fila_w,
        text="ε",
        width=5,
        command=poner_epsilon_w
    ).pack(side="left")

    # Campo para v
    fila_v = ttk.Frame(panel_cadenas)
    fila_v.pack(fill="x", pady=(0, 15))

    ttk.Label(
        fila_v,
        text="Cadena v:",
        width=12
    ).pack(side="left")

    entrada_v = ttk.Entry(
        fila_v,
        textvariable=valor_v
    )
    entrada_v.pack(
        side="left",
        fill="x",
        expand=True,
        padx=10
    )

    def poner_epsilon_v():
        valor_v.set("ε")
        entrada_v.focus_set()

    ttk.Button(
        fila_v,
        text="ε",
        width=5,
        command=poner_epsilon_v
    ).pack(side="left")

    # Validación de las dos cadenas
    def validar_cadenas():
        resultado_cadenas.set("")

        if not alfabeto:
            messagebox.showwarning(
                "Alfabeto pendiente",
                "Primero define un alfabeto en la pestaña Alfabeto.",
                parent=ventana
            )
            return

        w = interpretar_cadena(valor_w.get())
        v = interpretar_cadena(valor_v.get())

        if not pertenece_al_alfabeto(w, alfabeto):
            resultado_cadenas.set(
                "La cadena w no pertenece a Σ*."
            )
            messagebox.showerror(
                "Cadena inválida",
                "Corrige w: contiene símbolos que no están en el alfabeto.",
                parent=ventana
            )
            entrada_w.focus_set()
            return

        if not pertenece_al_alfabeto(v, alfabeto):
            resultado_cadenas.set(
                "La cadena v no pertenece a Σ*."
            )
            messagebox.showerror(
                "Cadena inválida",
                "Corrige v: contiene símbolos que no están en el alfabeto.",
                parent=ventana
            )
            entrada_v.focus_set()
            return

        resultado_cadenas.set(
            "w = " + mostrar_cadena(w) + " pertenece a Σ*."
            + "\nv = " + mostrar_cadena(v) + " pertenece a Σ*."
        )

    boton_validar = ttk.Button(
        panel_cadenas,
        text="Validar cadenas",
        command=validar_cadenas
    )
    boton_validar.pack(anchor="w", pady=(0, 15))

    etiqueta_resultado_cadenas = ttk.Label(
        panel_cadenas,
        textvariable=resultado_cadenas,
        wraplength=650,
        justify="left"
    )
    etiqueta_resultado_cadenas.pack(anchor="w")

    entrada_alfabeto.focus_set()

    ventana.mainloop()


if __name__ == "__main__":
    main()