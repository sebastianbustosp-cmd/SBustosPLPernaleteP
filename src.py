import argparse
import math
import os
import sys
import time

# Aumentar el límite de recursión para evitar StackOverflow con n grandes en recursivo
sys.setrecursionlimit(20000)

def obtener_coeficientes_carpeta(nombre_carpeta):
    """Calcula los coeficientes (a, b) a partir de las letras de la carpeta."""
    letras = ""
    for caracter in nombre_carpeta.lower():
        if "a" <= caracter <= "z":
            letras += caracter

    S = 0
    for letra in letras:
        posicion = ord(letra) - ord("a") + 1
        S += posicion

    if S == 0 or nombre_carpeta.lower() == "src":
        return 1, 1

    a = 1 + (S % 3)
    b = 1 + ((S // 3) % 3)
    return a, b


# --- ALGORITMOS (Basados exactamente en los pseudocódigos) ---

def recursivo_general(n: int, a: int, b: int) -> int:
    """Algoritmo A2: RECURSIVOGENERAL(n, a, b)"""
    if n < 2:
        return n
    else:
        return a * recursivo_general(n - 1, a, b) + b * recursivo_general(n - 2, a, b)


def iterativo_general(n: int, a: int, b: int) -> int:
    """Algoritmo A3: ITERATIVOGENERAL(n, a, b)"""
    if n == 0:
        return 0
    
    prev2 = 0
    prev1 = 1
    
    for _ in range(2, n + 1):
        actual = a * prev1 + b * prev2
        prev2 = prev1
        prev1 = actual
        
    return prev1


# --- ALGORITMO MATRICIAL (Incluido para cumplir con '--algo mat') ---

def mult_matriz(A, B):
    """Multiplica dos matrices 2x2."""
    return [
        [
            A[0][0] * B[0][0] + A[0][1] * B[1][0],
            A[0][0] * B[0][1] + A[0][1] * B[1][1],
        ],
        [
            A[1][0] * B[0][0] + A[1][1] * B[1][0],
            A[1][0] * B[0][1] + A[1][1] * B[1][1],
        ],
    ]

def potencia_matriz(M, n):
    """Exponenciación rápida de matrices (Algoritmo A4 del informe)."""
    if n == 1:
        return M
    
    R = potencia_matriz(M, n // 2)
    R = mult_matriz(R, R)
    
    if n % 2 != 0:
        R = mult_matriz(R, M)
        
    return R

def matricial_general(n: int, a: int, b: int) -> int:
    """Calcula G(n) usando la matriz de transición."""
    if n == 0:
        return 0
    
    M = [[a, b], [1, 0]]
    P = potencia_matriz(M, n)
    # G(n) es la entrada (2,1) de la matriz M^n (índice [1][0] en Python)
    return P[1][0]


# --- EJECUCIÓN PRINCIPAL ---

def main():
    parser = argparse.ArgumentParser(description="Calculador de recurrencias G(n)")
    parser.add_argument("--algo", choices=["rec", "iter", "mat"], required=True)
    parser.add_argument("--n", type=int, required=True)
    parser.add_argument("--a", type=int, default=None)
    parser.add_argument("--b", type=int, default=None)

    args = parser.parse_args()

    # Detección automática de la carpeta
    ruta_script = os.path.abspath(__file__)
    carpeta_src = os.path.dirname(ruta_script)
    carpeta_raiz = os.path.basename(os.path.dirname(carpeta_src))

    a_auto, b_auto = obtener_coeficientes_carpeta(carpeta_raiz)

    a = args.a if args.a is not None else a_auto
    b = args.b if args.b is not None else b_auto

    algo_map = {
        "rec": recursivo_general,
        "iter": iterativo_general,
        "mat": matricial_general
    }
    
    funcion_elegida = algo_map[args.algo]

    # Desactivar el recolector de basura es recomendado para mediciones más limpias
    import gc
    gc.disable()

    # Medición de tiempo de ejecución
    t_start = time.perf_counter_ns()
    val = funcion_elegida(args.n, a, b)
    t_end = time.perf_counter_ns()

    gc.enable()
    
    elapsed_sec = (t_end - t_start) / 1e9

    # Cálculo seguro de la cantidad de dígitos (evitando conversiones a string para n > 4300)
    if val == 0:
        num_digits = 1
    else:
        num_digits = math.floor(math.log10(abs(val))) + 1

    # Últimos 20 dígitos (aplicando módulo 10^20)
    last_20 = val % (10**20)

    # Imprimir formato exacto exigido por la pauta
    print(f"N: {args.n}")
    print(f"Cantidad de dígitos: {num_digits}")
    print(f"Últimos 20 dígitos: {last_20:020d}")
    print(f"Tiempo de ejecución: {elapsed_sec:.8f} s")


if __name__ == "__main__":
    main()