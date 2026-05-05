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
