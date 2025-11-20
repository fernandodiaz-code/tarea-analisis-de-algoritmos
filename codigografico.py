import random
import time
from typing import Callable, Iterable, List

import matplotlib.pyplot as plt

from codigo import max_gain_professor_array, max_gain_professor_hash


def generar_valores(longitud: int, minimo: int = 1, maximo: int = 100) -> List[int]:
    """Crea una lista de enteros aleatorios de longitud par.

    Args:
        longitud: Tamaño total de la lista (2n).
        minimo: Valor mínimo posible por porción.
        maximo: Valor máximo posible por porción.

    Returns:
        Lista de enteros aleatorios.
    """
    if longitud % 2 != 0:
        raise ValueError("La longitud debe ser par (2n).")
    return [random.randint(minimo, maximo) for _ in range(longitud)]


def medir_promedio(
    funcion: Callable[[List[int]], int],
    longitudes: Iterable[int],
    repeticiones: int,
) -> List[float]:
    """Mide el tiempo promedio de la función para cada longitud especificada."""
    promedios = []
    for longitud in longitudes:
        acumulado = 0.0
        for _ in range(repeticiones):
            valores = generar_valores(longitud)

            inicio = time.perf_counter()
            funcion(valores)
            fin = time.perf_counter()

            acumulado += fin - inicio
        promedios.append(acumulado / repeticiones)
    return promedios


def graficar_tiempos(
    longitudes: List[int],
    tiempos_array: List[float],
    tiempos_hash: List[float],
    nombre_archivo: str = "tiempos.png",
) -> None:
    """Genera y guarda el gráfico comparando ambos enfoques."""
    plt.figure(figsize=(8, 5))
    plt.plot(longitudes, tiempos_array, marker="o", label="Matriz 2D")
    plt.plot(longitudes, tiempos_hash, marker="s", label="Hash")

    plt.xlabel("Tamaño de la entrada (2n)")
    plt.ylabel("Tiempo promedio (s)")
    plt.title("Comparación de tiempos: matriz vs. hash")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.6)

    plt.tight_layout()
    plt.savefig(nombre_archivo, dpi=300)
    plt.close()


if __name__ == "__main__":
    random.seed(42)

    longitudes = list(range(6, 32, 2))
    repeticiones = 5

    tiempos_array = medir_promedio(max_gain_professor_array, longitudes, repeticiones)
    tiempos_hash = medir_promedio(max_gain_professor_hash, longitudes, repeticiones)

    graficar_tiempos(longitudes, tiempos_array, tiempos_hash)

    print("Longitudes:", longitudes)
    print("Tiempos promedio (matriz):", tiempos_array)
    print("Tiempos promedio (hash):", tiempos_hash)
    print("Gráfico guardado en tiempos.png")