# Taller 3 — Métodos Numéricos: Explicación del proyecto

## Estructura general del proyecto

```
taller3analisis/
├── main.py                  ← punto de entrada, ventana + navegación
├── core/
│   ├── gauss_seidel.py      ← algoritmo matemático (Punto 1)
│   └── lu_decomposition.py  ← algoritmo matemático (Punto 2)
└── ui/
    ├── gs_view.py           ← interfaz gráfica Gauss-Seidel
    └── lu_view.py           ← interfaz gráfica LU
```

Idea central: **separar la lógica matemática (core/) de la interfaz (ui/)**.
Esto permite probar los algoritmos desde consola sin necesidad de abrir la app.

---

## `core/gauss_seidel.py` — El algoritmo

**Problema que resuelve:** sistema lineal `Ax = b` de forma iterativa.

**Idea matemática:** se despeja cada `x_i` de su propia ecuación y se actualiza
usando los valores *más recientes* ya calculados en la misma iteración
(eso lo diferencia de Jacobi):

```
x_i = (b_i - Σ A[i][j]*x[j] para j≠i) / A[i][i]
```

**Flujo del código:**
1. Empieza con `error = inf` para garantizar que el `while` siempre entra al menos una vez
   - Iniciar con `error = 1` sería un error si la tolerancia es >= 1
2. En cada iteración: recorre las `n` ecuaciones, actualiza `x[i]` al instante,
   calcula el cambio (`|x_nuevo - x_viejo|`)
3. El **error global** es el mayor cambio individual (`max`)
4. Para cuando `error ≤ tolerancia` o se agotan las iteraciones
5. Retorna: solución, lista de iteraciones (para mostrar en tabla), y si convergió

**Punto clave:** la línea `solucion[i] = ...` escribe directamente en el vector
que se sigue leyendo en la misma iteración. Eso es lo que hace a Gauss-Seidel
más rápido que Jacobi (que usa una copia separada).

---

## `core/lu_decomposition.py` — El algoritmo

Tiene 4 funciones con responsabilidades claras:

### 1. `lu_descomponer`
Factoriza `A = L·U` usando el **algoritmo de Doolittle**:
- `L` = triangular inferior con **1s en la diagonal**
- `U` = triangular superior
- En cada paso `i`: primero calcula la fila `i` de `U`, luego la columna `i` de `L`
- Lanza `ValueError` si el pivote `U[i][i] == 0` (matriz singular)

### 2. `sustitucion_adelante`
Resuelve `L·d = b` de arriba hacia abajo:
```
d[0] = b[0] / L[0][0]
d[i] = (b[i] - Σ L[i][j]*d[j]) / L[i][i]
```

### 3. `sustitucion_atras`
Resuelve `U·x = d` de abajo hacia arriba:
```
x[n-1] = d[n-1] / U[n-1][n-1]
x[i]   = (d[i] - Σ U[i][j]*x[j]) / U[i][i]
```

### 4. `lu_resolver`
Orquesta los 3 pasos: descomponer → sustitución adelante → sustitución atrás.

### 5. `lu_calcular_inversa`
**Truco eficiente:** factoriza `A` una sola vez, luego resuelve `n` sistemas,
uno por cada **vector canónico** `eᵢ` (vector con un 1 en posición `i` y ceros
en el resto). Cada solución `xᵢ` es una columna de `A⁻¹`.
Al final, transpone para obtener la matriz por filas.

---

## `main.py` — Ventana principal

La clase `AppPrincipal` extiende `tk.Tk` (la ventana raíz de tkinter).

**Layout:**
- **Sidebar** izquierda (230px fijo) con botones de navegación
- **Área de contenido** derecha que ocupa el resto

**Navegación:**
- `_mostrar_vista()` destruye el frame activo y crea uno nuevo
- El indicador verde (barra de 3px) y el color del botón cambian para mostrar cuál está activo
- Las vistas se importan **lazy** (dentro del método) para no cargar todo al inicio

---

## `ui/gs_view.py` — Interfaz Gauss-Seidel

Clase `VistaGaussSeidel` extiende `tk.Frame`.

**Matriz dinámica:**
- Al cambiar `n` y presionar "Generar matriz", se destruyen todos los widgets del `card` y se recrean
- Almacena referencias a los `Entry` en listas: `entradas_A[i][j]`, `entradas_b[i]`, `entradas_x0[i]`
- Los valores iniciales `x₀` se pre-rellenan con `0`

**Flujo al calcular:**
1. `_leer()` valida y convierte todos los inputs a `float`/`int`
2. Llama a `gauss_seidel()` del core
3. `_mostrar()` formatea la tabla de iteraciones en un widget `Text` monoespaciado

**Tabla de resultados:** construye strings con `f-string` y alineación (`>12`, `>4`)
para que las columnas queden rectas. El widget `Text` se pone en `DISABLED`
para que el usuario no lo edite.

---

## `ui/lu_view.py` — Interfaz LU

Clase `VistaLU` extiende `tk.Frame`.

**Sistema de tabs manual:**
- Se crean 3 frames ocultos: "Matrices L y U", "Solución", "Matriz Inversa"
- `_mostrar_tab()` hace `pack_forget()` al tab anterior y `pack()` al nuevo
- Los tabs solo aparecen después de calcular

**Flujo al calcular:**
1. Lee inputs → llama `lu_resolver()` y `lu_calcular_inversa()`
2. Rellena los 3 tabs con texto formateado
3. Muestra el panel de tabs y activa el tab "L y U"

**Helper `_entry()`:** en macOS tkinter no muestra bordes en `Entry`, así que
se envuelve en un `Frame` de 1px de color para simular el borde visualmente.

---

## Flujo completo resumido

```
Usuario presiona "Calcular" (Gauss-Seidel)
        │
        ▼
ui/gs_view.py: _calcular()
  → _leer()          valida inputs, convierte a float
  → gauss_seidel()   algoritmo en core/ (devuelve sol, iters, conv)
  → _mostrar()       escribe tabla en widget Text
```

```
Usuario presiona "Calcular" (LU)
        │
        ▼
ui/lu_view.py: _calcular()
  → _leer()               valida inputs
  → lu_resolver()         L, U, d, x
  → lu_calcular_inversa() A⁻¹
  → _rellenar_*()         escribe en cada tab
```

---

## Puntos clave para destacar en clase

1. **Gauss-Seidel vs Jacobi:** la diferencia está en una sola línea —
   Gauss-Seidel actualiza `x[i]` inmediatamente y lo usa en la misma iteración.

2. **Truco de la inversa por LU:** en vez de hacer `n` factorizaciones completas,
   se factoriza `A` una sola vez y se resuelven `n` sistemas con los mismos `L` y `U`.
   Esto es mucho más eficiente.

3. **`error = float('inf')` al inicio:** garantiza que el `while` siempre entra
   al menos una vez, sin importar cuál sea la tolerancia del usuario.

4. **Separación core/ui:** los algoritmos en `core/` no saben nada de tkinter.
   Se pueden probar solos con `python test_algoritmos.py`.
