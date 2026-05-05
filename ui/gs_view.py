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
        ttk.Label(interior, text="x₀ inicial", style="Acento.TLabel").grid(
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
