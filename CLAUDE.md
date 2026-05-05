# Taller 3 — Métodos Numéricos

## Contexto
App de escritorio Python + tkinter. Sin librerías externas de UI.
Lee el outline.md para entender el proyecto completo antes de empezar.

## Lo que ya está implementado (Verifica que este todo bien, las importaciones mas que todo)
- `core/gauss_seidel.py`
  - función: gauss_seidel(matriz_A, vector_b, aproximacion_inicial, tolerancia, max_iteraciones)
  - retorna: solucion (list), iteraciones (list of dicts {numero, valores, error}), convergio (bool)

- `core/lu_decomposition.py`
  - función: lu_resolver(matriz_A, vector_b) → matriz_L, matriz_U, vector_d, vector_x
  - función: lu_calcular_inversa(matriz_A) → matriz_inversa, matriz_L, matriz_U
  - lanza ValueError si la matriz es singular

## Lo que falta construir
1. `ui/gs_view.py` — frame tkinter con inputs dinámicos y tabla de iteraciones
2. `ui/lu_view.py` — frame tkinter con inputs dinámicos y tabs de resultados
3. `main.py` — ventana principal con sidebar de navegación entre las dos vistas

## Reglas de implementación
- Python 3.9, solo librerías estándar (tkinter, math)
- Tema oscuro: bg=#0f1117, accent=#4f8ef7, texto=#e8eaf0, card=#1a1d27
- Variables y comentarios en español
- Inputs dinámicos: el grid de la matriz se regenera al cambiar n
- Manejo de errores: mostrar mensajes claros si el usuario ingresa datos inválidos
- NO usar numpy, scipy ni ninguna librería numérica externa

## Orden de construcción sugerido
1. main.py (ventana + navegación vacía)
2. ui/gs_view.py (vista completa Gauss-Seidel)
3. ui/lu_view.py (vista completa LU + Inversa)
4. Conectar todo y probar