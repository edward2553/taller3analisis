"""
Prueba rápida de los algoritmos antes de conectar la UI.
Sistema de ejemplo:
  4x₁ +  x₂ = 9
   x₁ + 3x₂ = 10
Solución exacta: x₁ = 1.727, x₂ = 2.757
"""
import sys
sys.path.insert(0, '/home/claude/metodos_numericos')

from core.gauss_seidel import gauss_seidel
from core.lu_decomposition import lu_resolver, lu_calcular_inversa

A = [
    [4.0, 1.0],
    [1.0, 3.0]
]
b = [9.0, 10.0]

print("=" * 50)
print("GAUSS-SEIDEL")
print("=" * 50)
solucion, iteraciones, convergio = gauss_seidel(
    matriz_A=A,
    vector_b=b,
    aproximacion_inicial=[0.0, 0.0],
    tolerancia=1e-4,
    max_iteraciones=15
)
for it in iteraciones:
    valores = [f"{v:.6f}" for v in it['valores']]
    print(f"  Iter {it['numero']:2d} | x = {valores} | error = {it['error']:.2e}")

print(f"\n  Convergió: {convergio}")
print(f"  Solución: {[round(v, 6) for v in solucion]}")

print()
print("=" * 50)
print("DESCOMPOSICIÓN LU")
print("=" * 50)
L, U, d, x = lu_resolver(matriz_A=A, vector_b=b)
print(f"  L = {L}")
print(f"  U = {U}")
print(f"  d (sustitución adelante) = {d}")
print(f"  x (solución final)       = {[round(v, 6) for v in x]}")

print()
print("=" * 50)
print("MATRIZ INVERSA (LU)")
print("=" * 50)
inversa, L, U = lu_calcular_inversa(matriz_A=A)
for fila in inversa:
    print(f"  {[round(v, 6) for v in fila]}")
