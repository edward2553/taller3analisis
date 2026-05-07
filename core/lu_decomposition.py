def lu_descomponer(matriz_A):
    n = len(matriz_A)

    matriz_L = [[1.0 if fila == col else 0.0 for col in range(n)] for fila in range(n)]  # L inicia como identidad
    matriz_U = [[0.0] * n for _ in range(n)]  # U inicia como matriz cero

    for i in range(n):

        # calcular fila i de U
        for j in range(i, n):
            suma_lu = sum(matriz_L[i][k] * matriz_U[k][j] for k in range(i))
            matriz_U[i][j] = matriz_A[i][j] - suma_lu

        if matriz_U[i][i] == 0:
            raise ValueError(
                f"El pivote U[{i}][{i}] es cero. "
                "La matriz es singular o esta mal condicionada."
            )

        # calcular columna i de L (parte debajo de la diagonal)
        for j in range(i + 1, n):
            suma_lu = sum(matriz_L[j][k] * matriz_U[k][i] for k in range(i))
            matriz_L[j][i] = (matriz_A[j][i] - suma_lu) / matriz_U[i][i]

    return matriz_L, matriz_U


def sustitucion_adelante(matriz_L, vector_b):
    # resuelve L*d = b de arriba hacia abajo (L es triangular inferior)
    n = len(matriz_L)
    vector_d = [0.0] * n

    vector_d[0] = vector_b[0] / matriz_L[0][0]

    for i in range(1, n):
        suma_anteriores = sum(matriz_L[i][j] * vector_d[j] for j in range(i))
        vector_d[i] = (vector_b[i] - suma_anteriores) / matriz_L[i][i]

    return vector_d


def sustitucion_atras(matriz_U, vector_d):
    # resuelve U*x = d de abajo hacia arriba (U es triangular superior)
    n = len(matriz_U)
    vector_x = [0.0] * n

    vector_x[n - 1] = vector_d[n - 1] / matriz_U[n - 1][n - 1]

    for i in range(n - 2, -1, -1):
        suma_posteriores = sum(matriz_U[i][j] * vector_x[j] for j in range(i + 1, n))
        vector_x[i] = (vector_d[i] - suma_posteriores) / matriz_U[i][i]

    return vector_x


def lu_resolver(matriz_A, vector_b):
    # resuelve Ax = b mediante los tres pasos: descomponer A=LU, sustitucion adelante, sustitucion atras
    matriz_L, matriz_U = lu_descomponer(matriz_A)
    vector_d = sustitucion_adelante(matriz_L, vector_b)
    vector_x = sustitucion_atras(matriz_U, vector_d)
    return matriz_L, matriz_U, vector_d, vector_x


def lu_calcular_inversa(matriz_A):
    # calcula A^-1 resolviendo n sistemas con vectores canonicos como terminos independientes
    n = len(matriz_A)

    # se factoriza A = LU una sola vez y se reutiliza para los n sistemas
    matriz_L, matriz_U = lu_descomponer(matriz_A)

    columnas_de_inversa = []

    for i in range(n):
        vector_canonico = [1.0 if j == i else 0.0 for j in range(n)]  # vector ei con 1 en posicion i

        vector_d = sustitucion_adelante(matriz_L, vector_canonico)
        columna_i = sustitucion_atras(matriz_U, vector_d)

        columnas_de_inversa.append(columna_i)

    # columnas_de_inversa[i] es la columna i de A^-1; se transpone para obtener la matriz por filas
    matriz_inversa = [
        [columnas_de_inversa[col][fila] for col in range(n)]
        for fila in range(n)
    ]

    return matriz_inversa, matriz_L, matriz_U
