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
