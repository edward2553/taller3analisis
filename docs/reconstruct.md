# Reconstrucción completa — Taller 3 Métodos Numéricos

Copia cada bloque de código en la ruta indicada para recrear la app exactamente como está.

## Estructura de carpetas

```
taller3analisis/
├── main.py
├── core/
│   ├── __init__.py
│   ├── gauss_seidel.py
│   └── lu_decomposition.py
└── ui/
    ├── __init__.py
    ├── gs_view.py
    └── lu_view.py
```

Para crear los `__init__.py` vacíos:

```bash
touch core/__init__.py ui/__init__.py
```

---

## main.py

```python
"""
main.py — Punto de entrada de la aplicación Métodos Numéricos.
"""

import tkinter as tk
import tkinter.ttk as ttk

BG        = "#f4fbf7"
CARD      = "#ffffff"
ACCENT    = "#3aa981"   # verde principal refinado
TEXTO     = "#1f2937"
TEXTO_DIM = "#6b7280"
BORDE     = "#d1e7dd"
ACTIVO_BG = "#d9f2e6"   # verde claro activo

class AppPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Métodos Numéricos — Taller")
        self.geometry("1160x700")
        self.minsize(900, 560)
        self.configure(bg=BG)

        

        self._indicadores = {}
        self._botones_nav = {}
        self.frame_activo = None

        self._construir_layout()
        self._mostrar_vista("gauss_seidel")

    # ── Layout ──────────────────────────────────────────────────────────────

    def _construir_layout(self):
        # Sidebar
        self.sidebar = tk.Frame(self, bg=CARD, width=230)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)

        tk.Frame(self.sidebar, bg=ACCENT, height=3).pack(fill=tk.X)

        ttk.Label(self.sidebar, text="Métodos\nNuméricos",
                  style="SidebarTitulo.TLabel",
                  anchor="w", padding=(20, 18)).pack(fill=tk.X)

        ttk.Label(self.sidebar, text="Taller 3  —  Análisis Numérico",
                  style="SidebarSub.TLabel",
                  anchor="w", padding=(20, 0)).pack(fill=tk.X)

        tk.Frame(self.sidebar, bg=BORDE, height=1).pack(fill=tk.X, padx=16, pady=16)

        ttk.Label(self.sidebar, text="MÉTODOS",
                  style="SidebarSec.TLabel",
                  anchor="w", padding=(20, 4)).pack(fill=tk.X)

        self._boton_nav("Gauss-Seidel", "gauss_seidel")
        self._boton_nav("Descomposición LU", "lu")

        # Área de contenido
        self.area = tk.Frame(self, bg=BG)
        self.area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def _boton_nav(self, texto, vista_id):
        fila = tk.Frame(self.sidebar, bg=CARD)
        fila.pack(fill=tk.X)

        indicador = tk.Frame(fila, bg=CARD, width=3)
        indicador.pack(side=tk.LEFT, fill=tk.Y)
        self._indicadores[vista_id] = indicador

        btn = tk.Button(fila, text=texto,
                        bg=CARD, fg=TEXTO_DIM,
                        activebackground=ACTIVO_BG, activeforeground=TEXTO,
                        relief=tk.FLAT, font=("Helvetica", 11),
                        anchor="w", padx=16, pady=12, cursor="hand2",
                        command=lambda: self._mostrar_vista(vista_id))
        btn.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self._botones_nav[vista_id] = btn

    def _mostrar_vista(self, vista_id):
        for vid, btn in self._botones_nav.items():
            activo = vid == vista_id
            btn.configure(bg=ACTIVO_BG if activo else CARD,
                          fg=TEXTO if activo else TEXTO_DIM)
            self._indicadores[vid].configure(bg=ACCENT if activo else CARD)

        if self.frame_activo:
            self.frame_activo.destroy()

        if vista_id == "gauss_seidel":
            from ui.gs_view import VistaGaussSeidel
            self.frame_activo = VistaGaussSeidel(self.area)
        else:
            from ui.lu_view import VistaLU
            self.frame_activo = VistaLU(self.area)

        self.frame_activo.pack(fill=tk.BOTH, expand=True)


if __name__ == "__main__":
    app = AppPrincipal()
    app.mainloop()
```

---

## core/gauss_seidel.py

```python
"""
Método de Gauss-Seidel
----------------------
Resuelve sistemas de ecuaciones lineales Ax = b de forma iterativa.
Basado en el pseudocódigo entregado por el docente.
"""


def gauss_seidel(matriz_A, vector_b, aproximacion_inicial, tolerancia, max_iteraciones):
    """
    Resuelve Ax = b usando el método iterativo de Gauss-Seidel.

    Parámetros:
        matriz_A           -- matriz cuadrada de coeficientes (lista de listas)
        vector_b           -- vector de términos independientes
        aproximacion_inicial -- vector x₀ con valores de partida
        tolerancia         -- error máximo aceptable para detener las iteraciones
        max_iteraciones    -- límite de iteraciones para evitar bucles infinitos

    Retorna:
        solucion      -- vector x con la solución aproximada
        iteraciones   -- lista de dicts con el detalle de cada iteración
        convergio     -- True si el error quedó por debajo de la tolerancia
    """
    n = len(matriz_A)

    # Trabajamos sobre una copia para no modificar el vector original
    solucion = aproximacion_inicial[:]

    iteraciones = []
    numero_iteracion = 0
    error_actual = float('inf')  # Empezamos con error infinito para entrar al ciclo

    # ── Ciclo principal ──────────────────────────────────────────────────────
    # Continúa mientras el error supere la tolerancia y no se agoten las iteraciones
    while error_actual > tolerancia and numero_iteracion < max_iteraciones:
        error_actual = 0  # Reiniciamos el error en cada iteración

        for i in range(n):
            valor_anterior = solucion[i]

            # Suma todos los términos A[i][j] * x[j] excepto cuando j == i
            # Usa los valores MÁS RECIENTES de x (característica clave de Gauss-Seidel)
            suma_otros_terminos = sum(
                matriz_A[i][j] * solucion[j]
                for j in range(n)
                if j != i
            )

            # Despeja x[i] de la ecuación i
            solucion[i] = (vector_b[i] - suma_otros_terminos) / matriz_A[i][i]

            # El error global es el mayor cambio individual entre iteraciones
            cambio = abs(solucion[i] - valor_anterior)
            error_actual = max(error_actual, cambio)

        numero_iteracion += 1

        # Guardamos el estado de esta iteración para mostrarlo en la UI
        iteraciones.append({
            "numero":   numero_iteracion,
            "valores":  solucion[:],
            "error":    error_actual
        })

    convergio = error_actual <= tolerancia
    return solucion, iteraciones, convergio
```

---

## core/lu_decomposition.py

```python
"""
Descomposición LU
-----------------
Factoriza una matriz A en L (triangular inferior) y U (triangular superior),
luego las usa para resolver sistemas y calcular la matriz inversa.
Basado en los pseudocódigos entregados por el docente.
"""


def lu_descomponer(matriz_A):
    """
    Factoriza A en L y U tal que A = L * U.

    L es triangular inferior con 1s en la diagonal.
    U es triangular superior.

    Parámetros:
        matriz_A -- matriz cuadrada n×n (lista de listas)

    Retorna:
        matriz_L, matriz_U

    Lanza:
        ValueError si U[i][i] = 0 (sistema mal condicionado)
    """
    n = len(matriz_A)

    # L empieza como identidad (1s en diagonal, 0s en el resto)
    matriz_L = [[1.0 if fila == col else 0.0 for col in range(n)] for fila in range(n)]

    # U empieza como matriz de ceros
    matriz_U = [[0.0] * n for _ in range(n)]

    for i in range(n):

        # ── Calcular fila i de U ─────────────────────────────────────────────
        for j in range(i, n):
            suma_lu = sum(matriz_L[i][k] * matriz_U[k][j] for k in range(i))
            matriz_U[i][j] = matriz_A[i][j] - suma_lu

        # Verificar que el pivote no sea cero (sistema mal condicionado)
        if matriz_U[i][i] == 0:
            raise ValueError(
                f"El pivote U[{i}][{i}] es cero. "
                "La matriz es singular o está mal condicionada."
            )

        # ── Calcular columna i de L (debajo de la diagonal) ─────────────────
        for j in range(i + 1, n):
            suma_lu = sum(matriz_L[j][k] * matriz_U[k][i] for k in range(i))
            matriz_L[j][i] = (matriz_A[j][i] - suma_lu) / matriz_U[i][i]

    return matriz_L, matriz_U


def sustitucion_adelante(matriz_L, vector_b):
    """
    Resuelve L * d = b usando sustitución hacia adelante (de arriba hacia abajo).

    Como L es triangular inferior, d[0] se despeja directo
    y cada d[i] solo depende de los valores anteriores ya calculados.

    Parámetros:
        matriz_L -- matriz triangular inferior
        vector_b -- vector de términos independientes

    Retorna:
        vector_d -- solución intermedia
    """
    n = len(matriz_L)
    vector_d = [0.0] * n

    # Primer elemento: despeje directo
    vector_d[0] = vector_b[0] / matriz_L[0][0]

    # Elementos siguientes: usan los d[j] ya calculados
    for i in range(1, n):
        suma_anteriores = sum(matriz_L[i][j] * vector_d[j] for j in range(i))
        vector_d[i] = (vector_b[i] - suma_anteriores) / matriz_L[i][i]

    return vector_d


def sustitucion_atras(matriz_U, vector_d):
    """
    Resuelve U * x = d usando sustitución hacia atrás (de abajo hacia arriba).

    Como U es triangular superior, x[n-1] se despeja directo
    y cada x[i] solo depende de los valores posteriores ya calculados.

    Parámetros:
        matriz_U -- matriz triangular superior
        vector_d -- vector resultado de la sustitución adelante

    Retorna:
        vector_x -- solución del sistema
    """
    n = len(matriz_U)
    vector_x = [0.0] * n

    # Último elemento: despeje directo
    vector_x[n - 1] = vector_d[n - 1] / matriz_U[n - 1][n - 1]

    # Elementos anteriores: usan los x[j] ya calculados (de abajo hacia arriba)
    for i in range(n - 2, -1, -1):
        suma_posteriores = sum(matriz_U[i][j] * vector_x[j] for j in range(i + 1, n))
        vector_x[i] = (vector_d[i] - suma_posteriores) / matriz_U[i][i]

    return vector_x


def lu_resolver(matriz_A, vector_b):
    """
    Resuelve Ax = b usando descomposición LU.

    Combina los tres pasos:
      1. Descomponer A = L * U
      2. Sustitución adelante: L * d = b
      3. Sustitución atrás:    U * x = d

    Parámetros:
        matriz_A -- matriz de coeficientes
        vector_b -- vector de términos independientes

    Retorna:
        matriz_L, matriz_U, vector_d, vector_x
    """
    matriz_L, matriz_U = lu_descomponer(matriz_A)
    vector_d = sustitucion_adelante(matriz_L, vector_b)
    vector_x = sustitucion_atras(matriz_U, vector_d)
    return matriz_L, matriz_U, vector_d, vector_x


def lu_calcular_inversa(matriz_A):
    """
    Calcula la matriz inversa de A usando descomposición LU.

    Estrategia (basada en el pseudocódigo del docente):
      - Factoriza A = L * U una sola vez
      - Resuelve n sistemas, uno por cada vector canónico eᵢ
        (eᵢ es un vector con 1 en la posición i y 0 en el resto)
      - Cada solución xᵢ es una columna de A⁻¹

    Parámetros:
        matriz_A -- matriz cuadrada n×n

    Retorna:
        matriz_inversa -- A⁻¹ como lista de listas
        matriz_L       -- triangular inferior de la factorización
        matriz_U       -- triangular superior de la factorización

    Lanza:
        ValueError si la matriz es singular (sistema mal condicionado)
    """
    n = len(matriz_A)

    # Factorizamos UNA SOLA VEZ y reutilizamos L y U para los n sistemas
    matriz_L, matriz_U = lu_descomponer(matriz_A)

    columnas_de_inversa = []

    for i in range(n):
        # Vector canónico eᵢ: todos ceros excepto un 1 en la posición i
        vector_canonico = [1.0 if j == i else 0.0 for j in range(n)]

        # Resolver L * d = eᵢ  →  luego  U * x = d
        vector_d = sustitucion_adelante(matriz_L, vector_canonico)
        columna_i = sustitucion_atras(matriz_U, vector_d)

        columnas_de_inversa.append(columna_i)

    # columnas_de_inversa[i] = columna i de A⁻¹
    # Transponemos para obtener la matriz por filas
    matriz_inversa = [
        [columnas_de_inversa[col][fila] for col in range(n)]
        for fila in range(n)
    ]

    return matriz_inversa, matriz_L, matriz_U
```

---

## ui/gs_view.py

```python
"""
ui/gs_view.py — Vista del método de Gauss-Seidel.
"""

import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from core.gauss_seidel import gauss_seidel

BG        = "#0f1117"
CARD      = "#1a1d27"
ACCENT    = "#4f8ef7"
TEXTO     = "#e8eaf0"
TEXTO_DIM = "#8b8fa8"
BORDE     = "#2a2d3a"
VERDE     = "#4caf7d"
ROJO      = "#f76f6f"

FUENTE      = ("Helvetica", 11)
FUENTE_MONO = ("Courier", 11)


class VistaGaussSeidel(tk.Frame):
    def __init__(self, padre):
        super().__init__(padre, bg=BG)
        self.entradas_A  = []
        self.entradas_b  = []
        self.entradas_x0 = []
        self._construir_ui()
        self._generar_matriz()

    # ── Layout ──────────────────────────────────────────────────────────────

    def _construir_ui(self):
        # Encabezado
        enc = tk.Frame(self, bg=CARD)
        enc.pack(fill=tk.X)
        ttk.Label(enc, text="Punto 1 — Método de Gauss-Seidel",
                  style="TituloCard.TLabel", anchor="w",
                  padding=(24, 14)).pack(fill=tk.X)
        tk.Frame(enc, bg=BORDE, height=1).pack(fill=tk.X)

        # Zona de inputs
        zona = tk.Frame(self, bg=BG)
        zona.pack(fill=tk.X, padx=24, pady=16)

        # Fila: n + generar
        fila_n = tk.Frame(zona, bg=BG)
        fila_n.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(fila_n, text="Número de ecuaciones (n):",
                  style="BG.TLabel").pack(side=tk.LEFT)
        self.var_n = tk.StringVar(value="3")
        ttk.Entry(fila_n, textvariable=self.var_n, width=4,
                  style="Input.TEntry").pack(side=tk.LEFT, padx=8)
        tk.Button(fila_n, text="Generar matriz",
                  command=self._generar_matriz, **_btn_sec()).pack(side=tk.LEFT)

        # Tarjeta de la matriz
        self.card = tk.Frame(zona, bg=CARD)
        self.card.pack(fill=tk.X, pady=(0, 10))

        # Parámetros
        fila_p = tk.Frame(zona, bg=BG)
        fila_p.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(fila_p, text="Tolerancia:",
                  style="BG.TLabel").pack(side=tk.LEFT)
        self.var_tol = tk.StringVar(value="0.0001")
        ttk.Entry(fila_p, textvariable=self.var_tol, width=10,
                  style="Input.TEntry").pack(side=tk.LEFT, padx=8)

        ttk.Label(fila_p, text="Máx. iteraciones:",
                  style="BG.TLabel").pack(side=tk.LEFT, padx=(20, 0))
        self.var_max = tk.StringVar(value="15")
        ttk.Entry(fila_p, textvariable=self.var_max, width=6,
                  style="Input.TEntry").pack(side=tk.LEFT, padx=8)

        tk.Button(zona, text="  Calcular  ",
                  command=self._calcular, **_btn_pri()).pack(anchor="w")

        # Zona de resultados
        res = tk.Frame(self, bg=BG)
        res.pack(fill=tk.BOTH, expand=True, padx=24, pady=(4, 12))

        tk.Frame(res, bg=BORDE, height=1).pack(fill=tk.X, pady=(0, 8))

        frame_txt = tk.Frame(res, bg=CARD)
        frame_txt.pack(fill=tk.BOTH, expand=True)

        sb_y = tk.Scrollbar(frame_txt, orient=tk.VERTICAL)
        sb_x = tk.Scrollbar(frame_txt, orient=tk.HORIZONTAL)
        self.txt = tk.Text(frame_txt, bg=CARD, fg=TEXTO, font=FUENTE_MONO,
                           relief=tk.FLAT, state=tk.DISABLED,
                           yscrollcommand=sb_y.set, xscrollcommand=sb_x.set,
                           wrap=tk.NONE)
        sb_y.configure(command=self.txt.yview)
        sb_x.configure(command=self.txt.xview)
        sb_y.pack(side=tk.RIGHT, fill=tk.Y)
        sb_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.txt.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.lbl_estado = ttk.Label(res, text="", style="BG.TLabel")
        self.lbl_estado.pack(fill=tk.X, pady=(6, 0))

    # ── Matriz dinámica ──────────────────────────────────────────────────────

    def _generar_matriz(self):
        try:
            n = int(self.var_n.get())
            if not (1 <= n <= 10):
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "n debe ser un entero entre 1 y 10.")
            return

        for w in self.card.winfo_children():
            w.destroy()
        self.entradas_A  = []
        self.entradas_b  = []
        self.entradas_x0 = []

        # Padding interior de la tarjeta con un frame interno
        interior = tk.Frame(self.card, bg=CARD)
        interior.pack(padx=16, pady=12)

        ttk.Label(interior, text="Matriz A", style="Acento.TLabel").grid(
            row=0, column=0, columnspan=n, sticky="w", pady=(0, 6))
        ttk.Label(interior, text="b", style="Acento.TLabel").grid(
            row=0, column=n+1, sticky="w", padx=(16, 0), pady=(0, 6))
        ttk.Label(interior, text="Valores iniciales", style="Acento.TLabel").grid(
            row=0, column=n+3, sticky="w", padx=(16, 0), pady=(0, 6))

        for i in range(n):
            fila_a = []
            for j in range(n):
                e = ttk.Entry(interior, width=7, style="Input.TEntry")
                e.grid(row=i+1, column=j, padx=2, pady=2)
                fila_a.append(e)
            self.entradas_A.append(fila_a)

            ttk.Label(interior, text="|",
                      style="Dim.TLabel").grid(row=i+1, column=n, padx=8)

            eb = ttk.Entry(interior, width=7, style="Input.TEntry")
            eb.grid(row=i+1, column=n+1, padx=2, pady=2)
            self.entradas_b.append(eb)

            ttk.Label(interior, text="|",
                      style="Dim.TLabel").grid(row=i+1, column=n+2, padx=8)

            ex = ttk.Entry(interior, width=7, style="Input.TEntry")
            ex.insert(0, "0")
            ex.grid(row=i+1, column=n+3, padx=2, pady=2)
            self.entradas_x0.append(ex)

        self._limpiar()

    # ── Lectura y validación ─────────────────────────────────────────────────

    def _leer(self):
        n = len(self.entradas_A)

        def leer_float(widget, nombre):
            v = widget.get().strip()
            if not v:
                raise ValueError(f"Falta el valor {nombre}.")
            return float(v)

        matriz_a  = [[leer_float(self.entradas_A[i][j], f"A[{i+1}][{j+1}]")
                      for j in range(n)] for i in range(n)]
        vector_b  = [leer_float(self.entradas_b[i],  f"b[{i+1}]")  for i in range(n)]
        vector_x0 = [leer_float(self.entradas_x0[i], f"x₀[{i+1}]") for i in range(n)]

        tol_s = self.var_tol.get().strip()
        if not tol_s:
            raise ValueError("Ingresa la tolerancia.")
        tol = float(tol_s)
        if tol <= 0:
            raise ValueError("La tolerancia debe ser mayor que cero.")

        mi_s = self.var_max.get().strip()
        if not mi_s:
            raise ValueError("Ingresa el máximo de iteraciones.")
        mi = int(mi_s)
        if mi < 1:
            raise ValueError("El máximo de iteraciones debe ser al menos 1.")

        return matriz_a, vector_b, vector_x0, tol, mi

    # ── Cálculo y visualización ──────────────────────────────────────────────

    def _calcular(self):
        try:
            args = self._leer()
        except ValueError as e:
            messagebox.showerror("Datos inválidos", str(e))
            return
        try:
            sol, iters, conv = gauss_seidel(*args)
        except ZeroDivisionError:
            messagebox.showerror("Error numérico",
                                 "División por cero — la diagonal de A no puede tener ceros.")
            return
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return
        self._mostrar(iters, sol, conv)

    def _mostrar(self, iters, sol, conv):
        n, w = len(sol), 12
        enc = (f"{'Iter':>4}  "
               + "".join(f"{'x'+str(k+1):>{w}}  " for k in range(n))
               + f"{'Error':>12}")
        sep = "─" * len(enc)
        lineas = [sep, enc, sep]
        for it in iters:
            linea = f"{it['numero']:>4}  "
            linea += "".join(f"{v:>{w}.6f}  " for v in it["valores"])
            linea += f"{it['error']:>12.4e}"
            lineas.append(linea)
        lineas.append(sep)

        self.txt.configure(state=tk.NORMAL)
        self.txt.delete("1.0", tk.END)
        self.txt.insert(tk.END, "\n".join(lineas))
        self.txt.configure(state=tk.DISABLED)

        estado = (f"✓  Convergió en {len(iters)} iteraciones." if conv
                  else f"✗  No convergió — máximo de {len(iters)} iteraciones alcanzado.")
        sol_txt = "     ".join(f"x{k+1} = {v:.6f}" for k, v in enumerate(sol))
        self.lbl_estado.configure(
            text=f"{estado}\nSolución:  {sol_txt}",
            foreground=VERDE if conv else ROJO)

    def _limpiar(self):
        self.txt.configure(state=tk.NORMAL)
        self.txt.delete("1.0", tk.END)
        self.txt.configure(state=tk.DISABLED)
        self.lbl_estado.configure(text="")


# ── Helpers ──────────────────────────────────────────────────────────────────

def _btn_pri():
    return {"bg": ACCENT, "fg": TEXTO, "activebackground": "#3a7be0",
            "activeforeground": TEXTO, "relief": tk.FLAT,
            "font": ("Helvetica", 11, "bold"), "padx": 22, "pady": 8, "cursor": "hand2"}


def _btn_sec():
    return {"bg": "#252a3d", "fg": TEXTO, "activebackground": "#2e3456",
            "activeforeground": TEXTO, "relief": tk.FLAT,
            "font": FUENTE, "padx": 14, "pady": 6, "cursor": "hand2"}
```

---

## ui/lu_view.py

```python
"""
ui/lu_view.py — Vista de Descomposición LU + Matriz Inversa.
"""

import tkinter as tk
from tkinter import messagebox
from core.lu_decomposition import lu_resolver, lu_calcular_inversa

BG        = "#0f1117"
CARD      = "#1a1d27"
ACCENT    = "#4f8ef7"
TEXTO     = "#e8eaf0"
TEXTO_DIM = "#8b8fa8"
BORDE     = "#2a2d3a"

FUENTE      = ("Helvetica", 11)
FUENTE_MONO = ("Courier", 11)

TABS = [
    ("lu",       "Matrices L y U"),
    ("solucion", "Solución"),
    ("inversa",  "Matriz Inversa"),
]


class VistaLU(tk.Frame):
    def __init__(self, padre):
        super().__init__(padre, bg=BG)
        self.entradas_A   = []
        self.entradas_b   = []
        self._tab_actual  = None
        self._frames_tab  = {}
        self._botones_tab = {}
        self._construir_ui()
        self._generar_matriz()

    # ── Layout ──────────────────────────────────────────────────────────────

    def _construir_ui(self):
        # Encabezado
        enc = tk.Frame(self, bg=CARD)
        enc.pack(fill=tk.X)
        tk.Label(enc, text="Punto 2 — Descomposición LU + Matriz Inversa",
                 bg=CARD, fg=TEXTO, font=("Helvetica", 13, "bold"),
                 anchor="w", padx=24, pady=14).pack(fill=tk.X)
        tk.Frame(enc, bg=BORDE, height=1).pack(fill=tk.X)

        # Zona de inputs
        zona = tk.Frame(self, bg=BG, padx=24, pady=16)
        zona.pack(fill=tk.X)

        # Fila: n + generar
        fila_n = tk.Frame(zona, bg=BG)
        fila_n.pack(fill=tk.X, pady=(0, 12))

        tk.Label(fila_n, text="Número de ecuaciones (n):",
                 bg=BG, fg=TEXTO, font=FUENTE).pack(side=tk.LEFT)
        self.var_n = tk.StringVar(value="3")
        marco_n, _ = _entry(fila_n, textvariable=self.var_n, width=4)
        marco_n.pack(side=tk.LEFT, padx=8)
        tk.Button(fila_n, text="Generar matriz",
                  command=self._generar_matriz, **_btn_sec()).pack(side=tk.LEFT)

        # Tarjeta de la matriz
        self.card = tk.Frame(zona, bg=CARD, padx=18, pady=14)
        self.card.pack(fill=tk.X, pady=(0, 12))

        # Botón calcular
        tk.Button(zona, text="  Calcular  ", command=self._calcular,
                  **_btn_pri()).pack(anchor="w")

        # Zona de resultados con tabs
        res = tk.Frame(self, bg=BG, padx=24)
        res.pack(fill=tk.BOTH, expand=True, pady=(4, 12))

        tk.Frame(res, bg=BORDE, height=1).pack(fill=tk.X, pady=(0, 8))

        self.panel_tabs = tk.Frame(res, bg=BG)
        self._construir_tabs(self.panel_tabs)
        self.panel_tabs.pack_forget()  # Oculto hasta calcular

    def _construir_tabs(self, padre):
        barra = tk.Frame(padre, bg=CARD)
        barra.pack(fill=tk.X)

        for tab_id, etiqueta in TABS:
            btn = tk.Button(
                barra, text=etiqueta,
                bg=CARD, fg=TEXTO_DIM,
                activebackground=ACCENT, activeforeground=TEXTO,
                relief=tk.FLAT, font=FUENTE,
                padx=18, pady=9, cursor="hand2",
                command=lambda t=tab_id: self._mostrar_tab(t),
            )
            btn.pack(side=tk.LEFT)
            self._botones_tab[tab_id] = btn

        tk.Frame(padre, bg=BORDE, height=1).pack(fill=tk.X)

        self.area_tabs = tk.Frame(padre, bg=CARD)
        self.area_tabs.pack(fill=tk.BOTH, expand=True)

        for tab_id, _ in TABS:
            frame = tk.Frame(self.area_tabs, bg=CARD)

            sb_y = tk.Scrollbar(frame, orient=tk.VERTICAL)
            sb_x = tk.Scrollbar(frame, orient=tk.HORIZONTAL)
            texto = tk.Text(frame, bg=CARD, fg=TEXTO, font=FUENTE_MONO,
                            relief=tk.FLAT, state=tk.DISABLED,
                            yscrollcommand=sb_y.set, xscrollcommand=sb_x.set,
                            wrap=tk.NONE)
            sb_y.configure(command=texto.yview)
            sb_x.configure(command=texto.xview)
            sb_y.pack(side=tk.RIGHT, fill=tk.Y)
            sb_x.pack(side=tk.BOTTOM, fill=tk.X)
            texto.pack(fill=tk.BOTH, expand=True, padx=12, pady=12)

            self._frames_tab[tab_id] = (frame, texto)

    def _mostrar_tab(self, tab_id):
        if self._tab_actual:
            self._frames_tab[self._tab_actual][0].pack_forget()
            self._botones_tab[self._tab_actual].configure(bg=CARD, fg=TEXTO_DIM)
        self._frames_tab[tab_id][0].pack(fill=tk.BOTH, expand=True)
        self._botones_tab[tab_id].configure(bg=ACCENT, fg=TEXTO)
        self._tab_actual = tab_id

    # ── Matriz dinámica ──────────────────────────────────────────────────────

    def _generar_matriz(self):
        try:
            n = int(self.var_n.get())
            if not (1 <= n <= 10):
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "n debe ser un entero entre 1 y 10.")
            return

        for w in self.card.winfo_children():
            w.destroy()
        self.entradas_A = []
        self.entradas_b = []

        _hdr(self.card, "Matriz A").grid(
            row=0, column=0, columnspan=n, sticky="w", pady=(0, 6))
        _hdr(self.card, "b").grid(
            row=0, column=n+1, sticky="w", padx=(16, 0), pady=(0, 6))

        for i in range(n):
            fila_a = []
            for j in range(n):
                marco, e = _entry(self.card, width=7)
                marco.grid(row=i+1, column=j, padx=2, pady=2)
                fila_a.append(e)
            self.entradas_A.append(fila_a)

            tk.Label(self.card, text="|", bg=CARD, fg=TEXTO_DIM,
                     font=FUENTE).grid(row=i+1, column=n, padx=10)

            marco_b, eb = _entry(self.card, width=7)
            marco_b.grid(row=i+1, column=n+1, padx=2, pady=2)
            self.entradas_b.append(eb)

        self.panel_tabs.pack_forget()
        self._tab_actual = None

    # ── Lectura y validación ─────────────────────────────────────────────────

    def _leer(self):
        n = len(self.entradas_A)

        def leer_float(widget, nombre):
            v = widget.get().strip()
            if not v:
                raise ValueError(f"Falta el valor {nombre}.")
            return float(v)

        matriz_a = [[leer_float(self.entradas_A[i][j], f"A[{i+1}][{j+1}]")
                     for j in range(n)] for i in range(n)]
        vector_b = [leer_float(self.entradas_b[i], f"b[{i+1}]") for i in range(n)]
        return matriz_a, vector_b

    # ── Cálculo y visualización ──────────────────────────────────────────────

    def _calcular(self):
        try:
            matriz_a, vector_b = self._leer()
        except ValueError as e:
            messagebox.showerror("Datos inválidos", str(e))
            return
        try:
            mat_l, mat_u, vec_d, vec_x = lu_resolver(matriz_a, vector_b)
            mat_inv, _, _ = lu_calcular_inversa(matriz_a)
        except ValueError as e:
            messagebox.showerror("Error numérico", str(e))
            return
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return

        self._rellenar_lu(mat_l, mat_u)
        self._rellenar_solucion(vec_d, vec_x)
        self._rellenar_inversa(mat_inv)

        self.panel_tabs.pack(fill=tk.BOTH, expand=True)
        self._mostrar_tab("lu")

    def _escribir(self, tab_id, contenido):
        _, texto = self._frames_tab[tab_id]
        texto.configure(state=tk.NORMAL)
        texto.delete("1.0", tk.END)
        texto.insert(tk.END, contenido)
        texto.configure(state=tk.DISABLED)

    def _rellenar_lu(self, mat_l, mat_u):
        n = len(mat_l)
        w = 10
        ancho = n * w + (n - 1) * 2
        lineas = [f"{'L':^{ancho}}        {'U':^{ancho}}", ""]
        for i in range(n):
            fl = "  ".join(f"{v:{w}.4f}" for v in mat_l[i])
            fu = "  ".join(f"{v:{w}.4f}" for v in mat_u[i])
            lineas.append(f"{fl}        {fu}")
        self._escribir("lu", "\n".join(lineas))

    def _rellenar_solucion(self, vec_d, vec_x):
        lineas = ["d  — sustitución adelante  (resuelve L·d = b):", ""]
        for i, v in enumerate(vec_d):
            lineas.append(f"  d{i+1} = {v:.6f}")
        lineas += ["", "─" * 44, "", "x  — solución final  (resuelve U·x = d):", ""]
        for i, v in enumerate(vec_x):
            lineas.append(f"  x{i+1} = {v:.6f}")
        self._escribir("solucion", "\n".join(lineas))

    def _rellenar_inversa(self, mat_inv):
        w = 10
        lineas = ["A⁻¹ =", ""]
        for fila in mat_inv:
            lineas.append("  " + "  ".join(f"{v:{w}.4f}" for v in fila))
        self._escribir("inversa", "\n".join(lineas))


# ── Helpers ──────────────────────────────────────────────────────────────────

def _entry(padre, **kwargs):
    """Entry enmarcado en un Frame de 1px — siempre visible en macOS."""
    marco = tk.Frame(padre, bg="#3a4060", padx=1, pady=1)
    e = tk.Entry(marco, bg="#1e2235", fg=TEXTO, insertbackground=TEXTO,
                 relief=tk.FLAT, font=FUENTE_MONO, **kwargs)
    e.pack(fill=tk.BOTH)
    return marco, e


def _btn_pri():
    return {"bg": ACCENT, "fg": TEXTO, "activebackground": "#3a7be0",
            "activeforeground": TEXTO, "relief": tk.FLAT,
            "font": ("Helvetica", 11, "bold"), "padx": 22, "pady": 8, "cursor": "hand2"}


def _btn_sec():
    return {"bg": "#252a3d", "fg": TEXTO, "activebackground": "#2e3456",
            "activeforeground": TEXTO, "relief": tk.FLAT,
            "font": FUENTE, "padx": 14, "pady": 6, "cursor": "hand2"}


def _hdr(padre, texto):
    return tk.Label(padre, text=texto, bg=CARD, fg=ACCENT,
                    font=("Helvetica", 10, "bold"))
```

---

## Ejecutar la app

```bash
python main.py
```

Requiere Python 3.9+ con tkinter incluido (viene por defecto en la instalación estándar).
