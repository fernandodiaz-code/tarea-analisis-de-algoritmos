# codigohash.py
from math import inf

def max_gain_professor_hash(values):
    n2 = len(values)
    if n2 % 2 != 0:
        raise ValueError("La lista debe tener longitud par (2n).")

    n = n2 // 2
    S = values + values
    N = len(S)

    pref = [0] * (N + 1)
    for i in range(N):
        pref[i+1] = pref[i] + S[i]

    def SUM(l, r):
        return pref[r+1] - pref[l]

    memo = {}

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

    return total - best_sister


if __name__ == "__main__":
    vals = [1, 100, 1, 1, 1, 100]
    print("Hash ->", max_gain_professor_hash(vals))
