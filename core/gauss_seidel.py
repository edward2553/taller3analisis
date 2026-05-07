"""
Método de Gauss-Seidel
----------------------
Resuelve sistemas de ecuaciones lineales Ax = b de forma iterativa.
"""

def gauss_seidel(matriz_A_coeficientes, vector_b_terminos_independientes, aproximacion_inicial, tolerancia, max_iteraciones):
    """
    Resuelve Ax = b usando el método iterativo de Gauss-Seidel.

    Parámetros:
        matriz_A           -- matriz cuadrada de coeficientes (lista de listas)
        vector_b           -- vector de términos independientes (lista)
        aproximacion_inicial -- vector x₀ con valores de partida, estos son los valores independientes 
        tolerancia         -- error máximo aceptable para detener las iteraciones
        max_iteraciones    -- límite de iteraciones para evitar bucles infinitos

    Retorna:
        solucion      -- vector x con la solución aproximada
        iteraciones   -- lista con el detalle de cada iteración
    """
    n_de_ecuaciones = len(matriz_A_coeficientes)

    # Trabajamos sobre una copia para no modificar el vector original
    solucion = aproximacion_inicial[:]

    iteraciones = []
    numero_iteracion = 0
    error_actual = float('inf')  # Empezamos con error infinito para entrar al ciclo

    # ── Ciclo principal ──────────────────────────────────────────────────────
    # Continúa mientras el error supere la tolerancia y no se alcance el máximo de iteraciones
    while error_actual > tolerancia and numero_iteracion < max_iteraciones:
        error_actual = 0  # Reiniciamos el error en cada iteración

        for i in range(n_de_ecuaciones):
            valor_anterior = solucion[i]

            # Suma todos los términos A[i][j] * x[j] excepto cuando j == i
            # Usa los valores MÁS RECIENTES de x (característica clave de Gauss-Seidel)
            suma_otros_terminos = sum(
                matriz_A_coeficientes[i][j] * solucion[j]
                for j in range(n_de_ecuaciones)
                if j != i
            )

            # Despeja x[i] de la ecuación i
            solucion[i] = (vector_b_terminos_independientes[i] - suma_otros_terminos) / matriz_A_coeficientes[i][i]

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
