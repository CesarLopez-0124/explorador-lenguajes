import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText


MAX_RESULTADOS = 10000
MAX_LONGITUD = 100


# =========================================================
# ALFABETO Y REPRESENTACIÓN
# =========================================================

def validar_alfabeto(texto):
    simbolos = []

    for elemento in texto.split(","):
        simbolo = elemento.strip()

        if simbolo == "":
            raise ValueError("El alfabeto no puede tener elementos vacíos.")

        if simbolo in ("ε", "∅"):
            raise ValueError("ε y ∅ están reservados para representar vacíos.")

        if len(simbolo) != 1:
            raise ValueError("Escribe un solo carácter por símbolo.")

        if simbolo in simbolos:
            raise ValueError("El símbolo '" + simbolo + "' está repetido.")

        simbolos.append(simbolo)

    return simbolos


def longitud(cadena):
    cantidad = 0

    for simbolo in cadena:
        cantidad = cantidad + 1

    return cantidad


def cardinalidad(elementos):
    cantidad = 0

    for elemento in elementos:
        cantidad = cantidad + 1

    return cantidad


def mostrar_cadena(cadena):
    if cadena == "":
        return "ε"

    return cadena


def ordenar_cadenas(cadenas):
    # Ordenamiento por inserción:
    # primero longitud y después orden lexicográfico.
    ordenadas = []

    for cadena in cadenas:
        posicion = 0

        while posicion < cardinalidad(ordenadas):
            actual = ordenadas[posicion]

            if longitud(cadena) < longitud(actual):
                break

            if longitud(cadena) == longitud(actual) and cadena < actual:
                break

            posicion = posicion + 1

        ordenadas.insert(posicion, cadena)

    return ordenadas


def representar_conjunto(elementos):
    if cardinalidad(elementos) == 0:
        return "∅"

    texto = "{"
    primero = True

    for elemento in ordenar_cadenas(elementos):
        if not primero:
            texto = texto + ", "

        texto = texto + mostrar_cadena(elemento)
        primero = False

    return texto + "}"


def describir_conjunto(nombre, elementos):
    return (
        nombre + " = " + representar_conjunto(elementos)
        + "\nCardinalidad: " + str(cardinalidad(elementos))
    )


def agregar_sin_repetir(elementos, elemento):
    if elemento not in elementos:
        if cardinalidad(elementos) >= MAX_RESULTADOS:
            raise ValueError(
                "El resultado supera 10 000 cadenas distintas. "
                "Reduce el alfabeto, el lenguaje o el exponente."
            )

        elementos.append(elemento)


# =========================================================
# CADENAS
# =========================================================

def interpretar_cadena(texto):
    if texto == "ε":
        return ""

    return texto


def pertenece_al_alfabeto(cadena, alfabeto):
    for simbolo in cadena:
        if simbolo not in alfabeto:
            return False

    return True


def leer_cadena(texto, alfabeto):
    cadena = interpretar_cadena(texto)

    if longitud(cadena) > MAX_LONGITUD:
        raise ValueError("Introduce una cadena de hasta 100 símbolos.")

    if not pertenece_al_alfabeto(cadena, alfabeto):
        raise ValueError(
            "La cadena " + repr(texto) + " no pertenece a Σ*. "
            "Corrige los símbolos que no están en el alfabeto."
        )

    return cadena


def leer_exponente(texto):
    try:
        numero = int(texto)
    except ValueError:
        raise ValueError("El exponente debe ser un número entero.")

    if numero < 0 or numero > 4:
        raise ValueError("El exponente debe estar entre 0 y 4.")

    return numero


def concatenar_cadenas(w, v):
    resultado = ""

    for simbolo in w:
        resultado = resultado + simbolo

    for simbolo in v:
        resultado = resultado + simbolo

    return resultado


def inversa(cadena):
    resultado = ""

    for simbolo in cadena:
        resultado = simbolo + resultado

    return resultado


def potencia_cadena(cadena, n):
    resultado = ""

    for repeticion in range(n):
        resultado = concatenar_cadenas(resultado, cadena)

    return resultado


def prefijos(cadena):
    resultado = [""]
    prefijo = ""

    for simbolo in cadena:
        prefijo = prefijo + simbolo
        resultado.append(prefijo)

    return resultado


def sufijos(cadena):
    resultado = [""]

    for inicio in range(longitud(cadena)):
        sufijo = ""

        for posicion in range(inicio, longitud(cadena)):
            sufijo = sufijo + cadena[posicion]

        resultado.append(sufijo)

    return resultado


def subcadenas(cadena):
    resultado = [""]

    for inicio in range(longitud(cadena)):
        subcadena = ""

        for fin in range(inicio, longitud(cadena)):
            subcadena = subcadena + cadena[fin]
            agregar_sin_repetir(resultado, subcadena)

    return resultado


def es_palindromo(cadena):
    return cadena == inversa(cadena)


# =========================================================
# GENERACIÓN DEL ALFABETO
# =========================================================

def generar_sigma_n(alfabeto, n):
    resultado = [""]

    for paso in range(n):
        nuevas = []

        for cadena in resultado:
            for simbolo in alfabeto:
                nueva = concatenar_cadenas(cadena, simbolo)
                agregar_sin_repetir(nuevas, nueva)

        resultado = nuevas

    return resultado


def generar_sigma_acotada(alfabeto, n, incluir_epsilon):
    resultado = []

    if incluir_epsilon:
        resultado.append("")

    for exponente in range(1, n + 1):
        cadenas = generar_sigma_n(alfabeto, exponente)

        for cadena in cadenas:
            agregar_sin_repetir(resultado, cadena)

    return resultado


# =========================================================
# LENGUAJES FINITOS
# =========================================================

def leer_lenguaje(texto, alfabeto):
    if texto.strip() == "" or texto.strip() == "∅":
        return []

    lenguaje = []

    for elemento in texto.split(","):
        palabra = elemento.strip()

        if palabra == "":
            raise ValueError(
                "Hay un elemento vacío entre comas. "
                "Escribe ε si deseas incluir la cadena vacía."
            )

        cadena = leer_cadena(palabra, alfabeto)
        agregar_sin_repetir(lenguaje, cadena)

    return lenguaje


def union(l1, l2):
    resultado = []

    for cadena in l1:
        agregar_sin_repetir(resultado, cadena)

    for cadena in l2:
        agregar_sin_repetir(resultado, cadena)

    return resultado


def interseccion(l1, l2):
    resultado = []

    for cadena in l1:
        if cadena in l2:
            agregar_sin_repetir(resultado, cadena)

    return resultado


def diferencia(l1, l2):
    resultado = []

    for cadena in l1:
        if cadena not in l2:
            agregar_sin_repetir(resultado, cadena)

    return resultado


def concatenar_lenguajes(l1, l2):
    resultado = []

    for w in l1:
        for v in l2:
            cadena = concatenar_cadenas(w, v)
            agregar_sin_repetir(resultado, cadena)

    return resultado


def potencia_lenguaje(lenguaje, n):
    # L^0 = {ε}, incluso si L es vacío.
    resultado = [""]

    for paso in range(n):
        resultado = concatenar_lenguajes(resultado, lenguaje)

    return resultado


def cerradura_acotada(lenguaje, n, incluir_epsilon):
    resultado = []
    potencia_actual = [""]

    if incluir_epsilon:
        resultado.append("")

    for paso in range(1, n + 1):
        potencia_actual = concatenar_lenguajes(
            potencia_actual,
            lenguaje
        )
        resultado = union(resultado, potencia_actual)

    return resultado


# =========================================================
# EJEMPLOS DE CHOMSKY
# =========================================================

def pertenece_a_estrella_b_estrella(cadena):
    aparecio_b = False

    for simbolo in cadena:
        if simbolo == "b":
            aparecio_b = True
        elif simbolo == "a":
            if aparecio_b:
                return False
        else:
            return False

    return True


def pertenece_an_bn(cadena):
    cantidad_a = 0
    cantidad_b = 0
    aparecio_b = False

    for simbolo in cadena:
        if simbolo == "a":
            if aparecio_b:
                return False

            cantidad_a = cantidad_a + 1

        elif simbolo == "b":
            aparecio_b = True
            cantidad_b = cantidad_b + 1

        else:
            return False

    return cantidad_a == cantidad_b


def pertenece_an_bn_cn(cadena):
    cantidad_a = 0
    cantidad_b = 0
    cantidad_c = 0
    fase = "a"

    for simbolo in cadena:
        if simbolo == "a":
            if fase != "a":
                return False

            cantidad_a = cantidad_a + 1

        elif simbolo == "b":
            if fase == "c":
                return False

            fase = "b"
            cantidad_b = cantidad_b + 1

        elif simbolo == "c":
            fase = "c"
            cantidad_c = cantidad_c + 1

        else:
            return False

    return cantidad_a == cantidad_b == cantidad_c


TEXTO_CHOMSKY = """JERARQUÍA DE CHOMSKY

TIPO 3: LENGUAJES REGULARES
Gramática: regular, por ejemplo lineal por la derecha.
Autómata: autómata finito.
Ejemplo: a*b* = {a^i b^j | i, j >= 0}.
Acepta cualquier cantidad de a seguida de cualquier cantidad de b.
Ejemplos: ε, a, b, aaabb.
Rechaza: ba, abab.
Basta recordar si ya comenzó el bloque de b; no necesita contar.
Gramática de ejemplo:
S → aS | bB | ε
B → bB | ε

TIPO 2: LENGUAJES LIBRES DE CONTEXTO
Gramática: libre de contexto.
Autómata: autómata de pila.
Ejemplo: {a^n b^n | n >= 0}.
Debe haber igual cantidad de a y de b, en ese orden.
Ejemplos: ε, ab, aabb, aaabbb.
Rechaza: aab, abab.
Una pila permite guardar una marca por cada a y quitar una por cada b.
Este lenguaje es libre de contexto, pero no regular.
Gramática de ejemplo:
S → aSb | ε

TIPO 1: LENGUAJES SENSIBLES AL CONTEXTO
Gramática: sensible al contexto; puede expresarse con reglas
no contractivas, con la excepción habitual para ε.
Autómata: autómata linealmente acotado.
Ejemplo: {a^n b^n c^n | n >= 0}.
Debe haber tres bloques ordenados con igual cantidad de símbolos.
Ejemplos: ε, abc, aabbcc.
Rechaza: aabbc, acb.
Puede reconocerse marcando una a, una b y una c en cada recorrido,
usando una cantidad de memoria proporcional a la entrada.
Este lenguaje es sensible al contexto, pero no libre de contexto.

TIPO 0: LENGUAJES RECURSIVAMENTE ENUMERABLES
Gramática: no restringida.
Autómata: máquina de Turing.
Ejemplo: A_TM = {<M, w> | la máquina M acepta la entrada w}.
Una máquina universal simula M sobre w y acepta si M acepta.
Si M no acepta, la simulación podría no terminar.
A_TM es reconocible, pero indecidible; por ello no es de tipo 1.
Este ejemplo se explica, pero no se implementa un decisor general.

RELACIÓN ENTRE LOS TIPOS
Tipo 3 ⊂ Tipo 2 ⊂ Tipo 1 ⊂ Tipo 0.
Las clases están incluidas unas dentro de otras.
Los ejemplos se presentan según su clase más restrictiva.

En los verificadores siguientes usamos n >= 0:
ε pertenece a los tres ejemplos.
Estos ejemplos tienen alfabetos fijos {a,b} y {a,b,c};
son independientes del alfabeto definido en la primera pestaña.
"""


# =========================================================
# AYUDAS PARA LA INTERFAZ
# =========================================================

def crear_salida(panel):
    salida = ScrolledText(
        panel,
        height=10,
        wrap="word",
        font=("Arial", 11)
    )
    salida.pack(fill="both", expand=True, pady=(10, 0))
    salida.configure(state="disabled")
    return salida


def escribir_salida(salida, texto):
    salida.configure(state="normal")
    salida.delete("1.0", tk.END)
    salida.insert("1.0", texto)
    salida.configure(state="disabled")


def crear_entrada(panel, etiqueta, boton=None, valor_boton=""):
    fila = ttk.Frame(panel)
    fila.pack(fill="x", pady=5)

    ttk.Label(
        fila,
        text=etiqueta,
        width=15
    ).pack(side="left")

    variable = tk.StringVar()

    entrada = ttk.Entry(fila, textvariable=variable)
    entrada.pack(side="left", fill="x", expand=True, padx=8)

    if boton is not None:
        def colocar_valor():
            variable.set(valor_boton)
            entrada.focus_set()

        ttk.Button(
            fila,
            text=boton,
            width=6,
            command=colocar_valor
        ).pack(side="left")

    return variable


def crear_exponente(panel, etiqueta):
    fila = ttk.Frame(panel)
    fila.pack(fill="x", pady=5)

    ttk.Label(fila, text=etiqueta).pack(side="left")

    variable = tk.StringVar(value="2")

    ttk.Spinbox(
        fila,
        from_=0,
        to=4,
        textvariable=variable,
        width=5
    ).pack(side="left", padx=10)

    return variable


# =========================================================
# VENTANA PRINCIPAL
# =========================================================

def main():
    ventana = tk.Tk()
    ventana.title("Explorador de alfabetos, cadenas y lenguajes")
    ventana.geometry("1000x720")
    ventana.minsize(850, 600)

    alfabeto = []

    ttk.Label(
        ventana,
        text="Explorador de alfabetos, cadenas y lenguajes",
        font=("Arial", 18, "bold")
    ).pack(pady=(15, 8))

    estado_alfabeto = tk.StringVar(
        value="Alfabeto actual: sin definir"
    )

    ttk.Label(
        ventana,
        textvariable=estado_alfabeto,
        wraplength=800
    ).pack(pady=(0, 10))

    pestanas = ttk.Notebook(ventana)
    pestanas.pack(fill="both", expand=True, padx=15, pady=(0, 15))

    panel_alfabeto = ttk.Frame(pestanas, padding=15)
    panel_cadenas = ttk.Frame(pestanas, padding=15)
    panel_generacion = ttk.Frame(pestanas, padding=15)
    panel_lenguajes = ttk.Frame(pestanas, padding=15)
    panel_chomsky = ttk.Frame(pestanas, padding=15)

    pestanas.add(panel_alfabeto, text="Alfabeto")
    pestanas.add(panel_cadenas, text="Cadenas")
    pestanas.add(panel_generacion, text="Generación")
    pestanas.add(panel_lenguajes, text="Lenguajes finitos")
    pestanas.add(panel_chomsky, text="Jerarquía de Chomsky")

    # Esta lista permite limpiar resultados al cambiar el alfabeto.
    salidas_dependientes = []

    def exigir_alfabeto():
        if not alfabeto:
            raise ValueError("Primero guarda un alfabeto.")

    def ejecutar(salida, operacion):
        # Si una entrada falla, no dejamos un resultado viejo visible.
        escribir_salida(salida, "")

        try:
            texto = operacion()
        except ValueError as error:
            escribir_salida(salida, "Error: " + str(error))
            messagebox.showerror(
                "Revisa los datos",
                str(error),
                parent=ventana
            )
            return

        escribir_salida(salida, texto)

    # -----------------------------------------------------
    # PESTAÑA ALFABETO
    # -----------------------------------------------------

    ttk.Label(
        panel_alfabeto,
        text=(
            "Símbolos de un carácter separados por comas. Ejemplo: a,b,c\n"
            "No se permiten repetidos, espacios como símbolos, ε ni ∅."
        ),
        wraplength=750
    ).pack(anchor="w", pady=(0, 10))

    valor_alfabeto = crear_entrada(panel_alfabeto, "Símbolos:")

    def guardar_alfabeto():
        nuevos = validar_alfabeto(valor_alfabeto.get())

        alfabeto.clear()

        for simbolo in nuevos:
            alfabeto.append(simbolo)

        estado_alfabeto.set(
            "Alfabeto actual: Σ = " + representar_conjunto(alfabeto)
        )

        for salida in salidas_dependientes:
            escribir_salida(
                salida,
                "Alfabeto actualizado. Vuelve a calcular."
            )

        return describir_conjunto("Σ", alfabeto)

    ttk.Button(
        panel_alfabeto,
        text="Guardar / cambiar alfabeto",
        command=lambda: ejecutar(salida_alfabeto, guardar_alfabeto)
    ).pack(anchor="w", pady=10)

    salida_alfabeto = crear_salida(panel_alfabeto)

    # -----------------------------------------------------
    # PESTAÑA CADENAS
    # -----------------------------------------------------

    ttk.Label(
        panel_cadenas,
        text=(
            "Escribe cadenas sin comas. Campo vacío o ε = cadena vacía.\n"
            "Máximo 100 símbolos por cadena. El exponente admite 0 a 4."
        )
    ).pack(anchor="w", pady=(0, 8))

    valor_w = crear_entrada(panel_cadenas, "Cadena w:", "ε", "ε")
    valor_v = crear_entrada(panel_cadenas, "Cadena v:", "ε", "ε")
    exponente_cadena = crear_exponente(panel_cadenas, "Exponente n:")

    def obtener_cadenas():
        exigir_alfabeto()
        w = leer_cadena(valor_w.get(), alfabeto)
        v = leer_cadena(valor_v.get(), alfabeto)
        return w, v

    def validar_cadenas():
        w, v = obtener_cadenas()

        return (
            "w = " + mostrar_cadena(w) + " pertenece a Σ*."
            + "\nv = " + mostrar_cadena(v) + " pertenece a Σ*."
        )

    def calcular_cadenas():
        w, v = obtener_cadenas()
        n = leer_exponente(exponente_cadena.get())

        wv = concatenar_cadenas(w, v)
        vw = concatenar_cadenas(v, w)

        texto = (
            "w = " + mostrar_cadena(w)
            + "\nv = " + mostrar_cadena(v)
            + "\n\n|w| = " + str(longitud(w))
            + "\n|v| = " + str(longitud(v))
            + "\nwᴿ = " + mostrar_cadena(inversa(w))
            + "\nvᴿ = " + mostrar_cadena(inversa(v))
            + "\nw^" + str(n) + " = "
            + mostrar_cadena(potencia_cadena(w, n))
            + "\nv^" + str(n) + " = "
            + mostrar_cadena(potencia_cadena(v, n))
            + "\n\nw·v = " + mostrar_cadena(wv)
            + "\nv·w = " + mostrar_cadena(vw)
        )

        if wv == vw:
            texto = texto + (
                "\nEn este caso coinciden. "
                "La concatenación no es conmutativa en general."
            )
        else:
            texto = texto + (
                "\nSon diferentes: este caso muestra "
                "que la concatenación no es conmutativa."
            )

        if es_palindromo(w):
            texto = texto + "\n\nw es palíndromo."
        else:
            texto = texto + "\n\nw no es palíndromo."

        if es_palindromo(v):
            texto = texto + "\nv es palíndromo."
        else:
            texto = texto + "\nv no es palíndromo."

        return texto

    def calcular_fragmentos():
        exigir_alfabeto()
        w = leer_cadena(valor_w.get(), alfabeto)

        return (
            "Resultados para w = " + mostrar_cadena(w)
            + "\n\n" + describir_conjunto("Prefijos", prefijos(w))
            + "\n\n" + describir_conjunto("Sufijos", sufijos(w))
            + "\n\n" + describir_conjunto("Subcadenas", subcadenas(w))
            + "\n\nLas subcadenas son fragmentos contiguos y no se repiten."
        )

    botones_cadenas = ttk.Frame(panel_cadenas)
    botones_cadenas.pack(fill="x", pady=8)

    ttk.Button(
        botones_cadenas,
        text="Validar cadenas",
        command=lambda: ejecutar(salida_cadenas, validar_cadenas)
    ).pack(side="left", padx=(0, 8))

    ttk.Button(
        botones_cadenas,
        text="Operaciones con w y v",
        command=lambda: ejecutar(salida_cadenas, calcular_cadenas)
    ).pack(side="left", padx=(0, 8))

    ttk.Button(
        botones_cadenas,
        text="Prefijos, sufijos y subcadenas de w",
        command=lambda: ejecutar(salida_cadenas, calcular_fragmentos)
    ).pack(side="left")

    salida_cadenas = crear_salida(panel_cadenas)
    salidas_dependientes.append(salida_cadenas)

    # -----------------------------------------------------
    # PESTAÑA GENERACIÓN
    # -----------------------------------------------------

    ttk.Label(
        panel_generacion,
        text=(
            "Σⁿ: cadenas de longitud exactamente n.\n"
            "Σ⁺ acotada: longitudes de 1 a n.\n"
            "Σ* acotada: longitudes de 0 a n, incluyendo ε."
        )
    ).pack(anchor="w", pady=(0, 10))

    exponente_sigma = crear_exponente(
        panel_generacion,
        "Longitud máxima n (0 a 4):"
    )

    def calcular_generacion():
        exigir_alfabeto()
        n = leer_exponente(exponente_sigma.get())

        exacta = generar_sigma_n(alfabeto, n)
        positiva = generar_sigma_acotada(alfabeto, n, False)
        kleene = generar_sigma_acotada(alfabeto, n, True)

        return (
            describir_conjunto("Σ^" + str(n), exacta)
            + "\n\n"
            + describir_conjunto("Σ⁺ hasta longitud " + str(n), positiva)
            + "\n\n"
            + describir_conjunto("Σ* hasta longitud " + str(n), kleene)
        )

    ttk.Button(
        panel_generacion,
        text="Generar conjuntos",
        command=lambda: ejecutar(salida_generacion, calcular_generacion)
    ).pack(anchor="w", pady=10)

    salida_generacion = crear_salida(panel_generacion)
    salidas_dependientes.append(salida_generacion)

    # -----------------------------------------------------
    # PESTAÑA LENGUAJES FINITOS
    # -----------------------------------------------------

    ttk.Label(
        panel_lenguajes,
        text=(
            "Separa las cadenas con comas: a,ab,ε\n"
            "ε incluye la cadena vacía. Campo vacío o ∅ = lenguaje vacío.\n"
            "En L₁* y L₁⁺, n limita el número de concatenaciones."
        )
    ).pack(anchor="w", pady=(0, 10))

    valor_l1 = crear_entrada(panel_lenguajes, "Lenguaje L₁:", "∅", "∅")
    valor_l2 = crear_entrada(panel_lenguajes, "Lenguaje L₂:", "∅", "∅")
    exponente_lenguaje = crear_exponente(panel_lenguajes, "Exponente n:")

    def calcular_lenguajes():
        exigir_alfabeto()

        l1 = leer_lenguaje(valor_l1.get(), alfabeto)
        l2 = leer_lenguaje(valor_l2.get(), alfabeto)
        n = leer_exponente(exponente_lenguaje.get())

        return (
            describir_conjunto("L₁", l1)
            + "\n\n" + describir_conjunto("L₂", l2)
            + "\n\n" + describir_conjunto("L₁ ∪ L₂", union(l1, l2))
            + "\n\n" + describir_conjunto("L₁ ∩ L₂", interseccion(l1, l2))
            + "\n\n" + describir_conjunto("L₁ − L₂", diferencia(l1, l2))
            + "\n\n" + describir_conjunto(
                "L₁·L₂", concatenar_lenguajes(l1, l2)
            )
            + "\n\n" + describir_conjunto(
                "L₁^" + str(n), potencia_lenguaje(l1, n)
            )
            + "\n\n" + describir_conjunto(
                "L₁* hasta " + str(n) + " concatenaciones",
                cerradura_acotada(l1, n, True)
            )
            + "\n\n" + describir_conjunto(
                "L₁⁺ hasta " + str(n) + " concatenaciones",
                cerradura_acotada(l1, n, False)
            )
            + "\n\nNota: si ε pertenece a L₁, también puede pertenecer a L₁⁺."
        )

    ttk.Button(
        panel_lenguajes,
        text="Calcular operaciones",
        command=lambda: ejecutar(salida_lenguajes, calcular_lenguajes)
    ).pack(anchor="w", pady=10)

    salida_lenguajes = crear_salida(panel_lenguajes)
    salidas_dependientes.append(salida_lenguajes)

    # -----------------------------------------------------
    # PESTAÑA CHOMSKY
    # -----------------------------------------------------

    ttk.Label(
        panel_chomsky,
        text=(
            "Prueba los ejemplos con a, b y c. "
            "No dependen del alfabeto de las otras pestañas."
        ),
        wraplength=750
    ).pack(anchor="w", pady=(0, 8))

    valor_ejemplo = crear_entrada(
        panel_chomsky,
        "Cadena:",
        "ε",
        "ε"
    )

    resultado_chomsky = tk.StringVar(
        value="Escribe una cadena para comprobar los tres ejemplos."
    )

    def verificar_ejemplos():
        cadena = interpretar_cadena(valor_ejemplo.get())

        if longitud(cadena) > MAX_LONGITUD:
            resultado_chomsky.set("Introduce hasta 100 símbolos.")
            return

        regular = pertenece_a_estrella_b_estrella(cadena)
        libre = pertenece_an_bn(cadena)
        sensible = pertenece_an_bn_cn(cadena)

        resultado_chomsky.set(
            "Cadena: " + mostrar_cadena(cadena)
            + "\na*b*: " + ("Sí pertenece" if regular else "No pertenece")
            + "\naⁿbⁿ: " + ("Sí pertenece" if libre else "No pertenece")
            + "\naⁿbⁿcⁿ: " + ("Sí pertenece" if sensible else "No pertenece")
        )

    ttk.Button(
        panel_chomsky,
        text="Verificar ejemplos",
        command=verificar_ejemplos
    ).pack(anchor="w", pady=8)

    ttk.Label(
        panel_chomsky,
        textvariable=resultado_chomsky,
        justify="left",
        wraplength=750
    ).pack(anchor="w")

    salida_teoria = crear_salida(panel_chomsky)
    escribir_salida(salida_teoria, TEXTO_CHOMSKY)

    ventana.mainloop()


if __name__ == "__main__":
    main()