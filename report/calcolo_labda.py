def calculate_lambda_7(lambda_1, p_7, p_15, epsilon=1e-300):
    """
    Calcola il valore di lambda_7 iterativamente fino a convergenza.

    Parametri:
    - lambda_1: Valore di lambda_1.
    - p_7: Valore di p_7.
    - p_15: Valore di p_15.
    - epsilon: Soglia di convergenza (default 1e-10).

    Ritorna:
    - Il valore di lambda_7 dopo la convergenza.
    """
    # Inizializza lambda_7 con un valore iniziale arbitrario (ad esempio 0)
    lambda_7 = 0
    diff = float('inf')  # Differenza iniziale grande

    while diff > epsilon:
        # Calcola la nuova somma ricorsiva con l'attuale lambda_7
        new_lambda_7 = lambda_1 * (1 - p_7) + recursive_sum(lambda_1, p_7, lambda_7, p_15, epsilon)

        # Calcola la differenza tra il vecchio e il nuovo valore di lambda_7
        diff = abs(new_lambda_7 - lambda_7)

        # Aggiorna lambda_7 per la prossima iterazione
        lambda_7 = new_lambda_7

    return lambda_7


def recursive_sum(lambda_1, p_7, lambda_7, p_15, epsilon, current_term=1, power=1):
    """
    Funzione ricorsiva per calcolare la somma infinita.

    Parametri:
    - lambda_1, p_7, lambda_7, p_15: Parametri del sistema.
    - epsilon: Soglia sotto la quale un termine è considerato insignificante.
    - current_term: Termini già sommati (default 1).
    - power: Potenza corrente di p_15 (default 1).

    Ritorna:
    - La somma calcolata ricorsivamente.
    """
    # Calcola il termine corrente
    term = lambda_7 * (p_15 ** power)

    # Se il termine corrente è minore di epsilon, fermati
    if term < epsilon:
        return 0

    # Continua con la somma ricorsiva
    return term + recursive_sum(lambda_1, p_7, lambda_7, p_15, epsilon, current_term + 1, power + 1)


lambda_1 = 0.092163242
p_7 = 0.0
p_15 = 0.377141

result = calculate_lambda_7(lambda_1, p_7, p_15)
print("lambda_7 =", result)