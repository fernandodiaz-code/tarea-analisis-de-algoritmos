from math import inf


def max_gain_professor_array(values):
    """
    Calcula la máxima ganancia que puede garantizar el profesor
    usando memoización con matriz 2D.

    :param values: lista de enteros, de largo 2n (torta circular)
    :return: entero, ganancia máxima garantizada del profesor
    """
    n2 = len(values)
    if n2 % 2 != 0:
        raise ValueError("La lista debe tener longitud par (2n).")

    n = n2 // 2

    # Duplicamos para linearizar el círculo.
    # S tendrá largo 4n, aunque solo usaremos índices hasta 3n-2.
    S = values + values
    N = len(S)

    # Prefix sums para SUM(l,r) en O(1)
    pref = [0] * (N + 1)
    for i in range(N):
        pref[i + 1] = pref[i] + S[i]

    def SUM(l, r):
        """Suma de S[l..r] inclusive."""
        return pref[r + 1] - pref[l]

    # memoW[l][r] guarda W(l,r) o None si no está calculado.
    memoW = [[None] * N for _ in range(N)]

    def W(l, r):
        """
        Máxima suma que puede asegurar el jugador de turno
        sobre el arco S[l..r].
        """
        if l == r:
            return S[l]

        if memoW[l][r] is not None:
            return memoW[l][r]

        total = SUM(l, r)
        L = r - l + 1

        # No se puede comer el arco completo, así que k va de 1 a L-1.
        best_rest = inf

        # Quitar un prefijo de longitud k
        for k in range(1, L):
            best_rest = min(best_rest, W(l + k, r))

        # Quitar un sufijo de longitud k
        for k in range(1, L):
            best_rest = min(best_rest, W(l, r - k))

        memoW[l][r] = total - best_rest
        return memoW[l][r]

    total = sum(values)

    # El profesor elige el semicírculo donde la hermana (jugando en el resto)
    # pueda asegurar lo mínimo posible.
    best_sister = inf
    for a in range(n2):  # todos los semicírculos de longitud n
        best_sister = min(best_sister, W(a, a + n - 1))

    professor_gain = total - best_sister
    return professor_gain


def max_gain_professor_hash(values):
    """
    Igual que max_gain_professor_array pero usando un diccionario
    para memoización en vez de una matriz 2D.
    """
    n2 = len(values)
    if n2 % 2 != 0:
        raise ValueError("La lista debe tener longitud par (2n).")

    n = n2 // 2

    S = values + values
    N = len(S)

    pref = [0] * (N + 1)
    for i in range(N):
        pref[i + 1] = pref[i] + S[i]

    def SUM(l, r):
        return pref[r + 1] - pref[l]

    memo = {}  # (l, r) -> W(l,r)

    def W(l, r):
        if l == r:
            return S[l]

        key = (l, r)
        if key in memo:
            return memo[key]

        total = SUM(l, r)
        L = r - l + 1
        best_rest = inf

        for k in range(1, L):
            best_rest = min(best_rest, W(l + k, r))
        for k in range(1, L):
            best_rest = min(best_rest, W(l, r - k))

        memo[key] = total - best_rest
        return memo[key]

    total = sum(values)

    best_sister = inf
    for a in range(n2):
        best_sister = min(best_sister, W(a, a + n - 1))

    professor_gain = total - best_sister
    return professor_gain


# --------------------------------------------------------------------
# Ejemplo de uso
# --------------------------------------------------------------------
if __name__ == "__main__":
    # Ejemplo: 2n porciones
    # Cambia estos valores por los de tu tarea para probar.
    values = [1, 100, 1, 1, 1, 100]  # largo 8 -> n = 4

    print("Valores de la torta:", values)

    prof_array = max_gain_professor_array(values)
    prof_hash = max_gain_professor_hash(values)

    print("Ganancia máxima profesor (matriz):", prof_array)
    print("Ganancia máxima profesor (hash):  ", prof_hash)
