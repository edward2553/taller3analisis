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
        self.configure(bg=BG, cursor="arrow")

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
