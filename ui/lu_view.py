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
