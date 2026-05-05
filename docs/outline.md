# Taller 3 — Métodos Numéricos

## Descripción general
Aplicación de escritorio en Python (tkinter) que implementa Gauss-Seidel y Descomposición LU
con cálculo de matriz inversa. Entregable como ejecutable para macOS (`.app`) y Windows (`.exe`)
via PyInstaller.

---

## Estrategia de desarrollo — Simple primero, pragmático

> Fase única: código limpio, funcional, sin patrones de diseño.
> Todo en una estructura mínima que sea fácil de explicar al docente.

```
metodos_numericos/
├── main.py                  # Entry point + ventana principal + navegación
├── core/
│   ├── gauss_seidel.py      # ✅ Algoritmo GS (implementado y probado)
│   └── lu_decomposition.py  # ✅ LU + sustituciones + inversa (implementado y probado)
└── ui/
    ├── gs_view.py           # Vista completa del Punto 1
    └── lu_view.py           # Vista completa del Punto 2
```

---

## Punto 1 — Gauss-Seidel

### Descripción
Programa que resuelve sistemas de ecuaciones lineales Ax = b de forma iterativa
mediante el método de Gauss-Seidel.

### Criterios de aceptación
El programa debe permitir al usuario:

- [ ] Ingresar el número de ecuaciones (n)
- [ ] Ingresar los coeficientes de la matriz A (grid dinámico n×n)
- [ ] Ingresar el vector de términos independientes b (n valores)
- [ ] Ingresar una aproximación inicial x₀ (n valores)
- [ ] Ingresar la tolerancia de error (ej: 1e-4)
- [ ] Ingresar el número máximo de iteraciones
- [ ] Ver los resultados de cada iteración en pantalla (tabla: iter, valores de x, error)
- [ ] Ver la solución final aproximada
- [ ] Ver si el método convergió o alcanzó el máximo de iteraciones

### Lógica — `core/gauss_seidel.py`
```
Entradas:  matriz_A, vector_b, aproximacion_inicial, tolerancia, max_iteraciones
Salidas:   solucion, lista_iteraciones, convergio (bool)

Por cada iteración:
  Por cada xᵢ:
    suma = Σ A[i][j] * x[j]  para j ≠ i  (usa valores más recientes)
    x[i] = (b[i] - suma) / A[i][i]
    error = max(error, |x[i] - x[i]_anterior|)
  Guardar { numero_iteracion, valores_x, error }
  Parar si error ≤ tolerancia  o  iteraciones ≥ max
```

---

## Punto 2 — Descomposición LU + Matriz Inversa

### Descripción
Programa que factoriza una matriz A en L y U, resuelve el sistema Ax = b
y calcula la matriz inversa A⁻¹.

### Criterios de aceptación
El programa debe permitir al usuario:

- [ ] Ingresar el número de ecuaciones (n)
- [ ] Ingresar los coeficientes de la matriz A (grid dinámico n×n)
- [ ] Ingresar el vector de términos independientes b (n valores)
- [ ] Ver las matrices L y U resultantes de la factorización
- [ ] Ver el vector d (resultado de sustitución adelante: Ld = b)
- [ ] Ver la solución x del sistema (resultado de sustitución atrás: Ux = d)
- [ ] Ver la matriz inversa A⁻¹
- [ ] Ver mensaje de error si la matriz es singular (sistema mal condicionado)

### Lógica — `core/lu_decomposition.py`
```
lu_descomponer(A)          → L, U
sustitucion_adelante(L, b) → d      (resuelve Ld = b, de arriba hacia abajo)
sustitucion_atras(U, d)    → x      (resuelve Ux = d, de abajo hacia arriba)
lu_resolver(A, b)          → L, U, d, x
lu_calcular_inversa(A)     → A⁻¹   (resuelve n sistemas con vectores canónicos eᵢ)
```

---

## UI — Diseño de pantallas

### Ventana principal (`main.py`)
- Sidebar izquierdo: botones para navegar entre Punto 1 y Punto 2
- Área derecha: frame que intercambia entre gs_view y lu_view
- Tema oscuro: fondo `#0f1117`, acento `#4f8ef7`

### Vista Gauss-Seidel (`ui/gs_view.py`)
```
[ Número de ecuaciones: [  ] ]  [ Generar matriz ]

Matriz A          | Vector b | Aprox. inicial x₀
[  ] [  ] [  ]   |   [  ]   |      [  ]
[  ] [  ] [  ]   |   [  ]   |      [  ]
[  ] [  ] [  ]   |   [  ]   |      [  ]

Tolerancia: [ 0.0001 ]    Máx. iteraciones: [ 15 ]

[ Calcular ]

─────────────────────────────────────────
Iter | x₁        | x₂        | Error
  1  | 2.250000  | 2.583333  | 2.58e+00
  2  | 1.604167  | 2.798611  | 6.46e-01
  ...
─────────────────────────────────────────
✅ Convergió en 6 iteraciones
Solución: x₁ = 1.5455   x₂ = 2.8182
```

### Vista LU + Inversa (`ui/lu_view.py`)
```
[ Número de ecuaciones: [  ] ]  [ Generar matriz ]

Matriz A          | Vector b
[  ] [  ] [  ]   |   [  ]
[  ] [  ] [  ]   |   [  ]
[  ] [  ] [  ]   |   [  ]

[ Calcular ]

[ Matrices L y U ] [ Solución ] [ Matriz Inversa ]  ← tabs

Tab Matrices L y U:
  L =                    U =
  1.00  0.00  0.00      4.00  1.00  2.00
  0.25  1.00  0.00      0.00  2.75  ...

Tab Solución:
  d (sustitución adelante): [9.0, 7.75]
  x (solución final):       [1.5455, 2.8182]

Tab Matriz Inversa:
   0.2727  -0.0909
  -0.0909   0.3636
```

---

## Empaquetado — Ejecutables

### macOS → `.app`
```bash
pip3 install pyinstaller
pyinstaller --onefile --windowed --name "MetodosNumericos" main.py
# Output: dist/MetodosNumericos.app
```

### Windows → `.exe`
```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name "MetodosNumericos" main.py
# Output: dist/MetodosNumericos.exe
```

> ⚠️ PyInstaller genera el ejecutable para el SO donde se ejecuta.
> Para generar el `.exe` se necesita correr el comando en Windows
> (o usar una VM / GitHub Actions con runner Windows).

---

## Checklist de entrega

- [x] `core/gauss_seidel.py` — implementado y probado
- [x] `core/lu_decomposition.py` — implementado y probado
- [ ] `ui/gs_view.py` — vista completa con tabla de iteraciones
- [ ] `ui/lu_view.py` — vista completa con tabs (L/U, solución, inversa)
- [ ] `main.py` — ventana principal con navegación entre puntos
- [ ] Prueba manual con el sistema del taller
- [ ] Ejecutable `.app` generado y probado en macOS
- [ ] Ejecutable `.exe` generado y probado en Windows
- [ ] Código fuente limpio con comentarios en español
