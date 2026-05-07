# Metodo iterativo para resolver sistemas Ax = b.
# A diferencia de Jacobi, cada x[i] se actualiza inmediatamente y se usa
# en el mismo barrido, lo que acelera la convergencia.
# Condicion suficiente de convergencia: A sea diagonal dominante.

def gauss_seidel(matriz_A_coeficientes, vector_b_terminos_independientes, aproximacion_inicial, tolerancia, max_iteraciones):
    n_de_ecuaciones = len(matriz_A_coeficientes)

    solucion = aproximacion_inicial[:]  # copia para no alterar el vector original

    iteraciones = []
    numero_iteracion = 0
    error_actual = float('inf')  # se inicializa en inf para entrar al while la primera vez

    # el ciclo termina cuando el error cae bajo la tolerancia o se agota el maximo de iteraciones
    while error_actual > tolerancia and numero_iteracion < max_iteraciones:
        error_actual = 0  # reiniciar error en cada iteracion

        for i in range(n_de_ecuaciones):
            valor_anterior = solucion[i]

            # suma de A[i][j]*x[j] para todos los j distintos de i.
            # usa los valores ya actualizados en esta misma iteracion (diferencia clave con Jacobi)
            suma_otros_terminos = sum(
                matriz_A_coeficientes[i][j] * solucion[j]
                for j in range(n_de_ecuaciones)
                if j != i
            )

            # despeje de x[i] de la ecuacion i-esima: x[i] = (b[i] - suma) / A[i][i]
            solucion[i] = (vector_b_terminos_independientes[i] - suma_otros_terminos) / matriz_A_coeficientes[i][i]

            # el error de la iteracion es el mayor cambio absoluto entre los x nuevos y los anteriores
            cambio = abs(solucion[i] - valor_anterior)
            error_actual = max(error_actual, cambio)

        numero_iteracion += 1

        # guardar snapshot de esta iteracion para mostrar tabla de convergencia en la UI
        iteraciones.append({
            "numero":   numero_iteracion,
            "valores":  solucion[:],
            "error":    error_actual
        })

    convergio = error_actual <= tolerancia
    return solucion, iteraciones, convergio
