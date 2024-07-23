import numpy as np

# Costanti per la simulazione del sistema
START = 0.0  # initial time */
STOP = 7 * 1440.0  # terminal time */

#STOP = 20.0
INFINITY = float(100.0 * STOP)  # must be much larger than STOP  */

#Triage
TASSO_DI_INGRESSO = 0.092163242  # ingressi (arrivals per unit time)
NUMERO_DI_SERVER_TRIAGE = 1
MEDIA_SERVIZIO_TRIAGE = 5.5

#Queue
NUMERO_DI_SERVER_QUEUE = 4
MEDIA_TASSO_DI_SERVIZIO_QUEUE = 16
TEMPO_LIMITE = 420

# Esami
NUMERO_DI_SERVER_ECG = 2
MEDIA_DI_SERVIZIO_ECG = 5

NUMERO_DI_SERVER_EMOCROMO = 1
MEDIA_DI_SERVIZIO_EMOCROMO = 5

NUMERO_DI_SERVER_ECOGRAFIA = 2
MEDIA_DI_SERVIZIO_ECOGRAFIA = 15

NUMERO_DI_SERVER_RADIOGRAFIA = 2
MEDIA_DI_SERVIZIO_RADIOGRAFIA = 25

NUMERO_DI_SERVER_TAC = 1
MEDIA_DI_SERVIZIO_TAC = 30

NUMERO_DI_SERVER_ALTRI_ESAMI = 3
MEDIA_DI_SERVIZIO_ALTRI_ESAMI = 35

MEDIA_DI_SERVIZIO_TRIAGE_ROSSO = 10
MEDIA_DI_SERVIZIO_TRIAGE_ARANCIONE = 57  # Tasso di servizio del server 1
MEDIA_DI_SERVIZIO_TRIAGE_BLU = 164  # Tasso di servizio del server 1
MEDIA_DI_SERVIZIO_TRIAGE_VERDE = 154  # Tasso di servizio del server 1
MEDIA_DI_SERVIZIO_TRIAGE_BIANCO = 15  # Tasso di servizio del server 1
SIGMA_DI_SERVIZIO_TRIAGE = 0.02  # Tasso di servizio del server 1

# Calcolo parametro lognormale
MU_VALORI = {
    1: 0,
    2: np.log(MEDIA_DI_SERVIZIO_TRIAGE_ARANCIONE) - (SIGMA_DI_SERVIZIO_TRIAGE ** 2) / 2,
    3: np.log(MEDIA_DI_SERVIZIO_TRIAGE_BLU) - (SIGMA_DI_SERVIZIO_TRIAGE ** 2) / 2,
    4: np.log(MEDIA_DI_SERVIZIO_TRIAGE_VERDE) - (SIGMA_DI_SERVIZIO_TRIAGE ** 2) / 2,
    5: np.log(MEDIA_DI_SERVIZIO_TRIAGE_BIANCO) - (SIGMA_DI_SERVIZIO_TRIAGE ** 2) / 2
}

# Deviazioni standard (SIGMA) per i vari codici di triage
SIGMA_VALORI = {
    1: 0,  # Esempio, metti un valore appropriato se diverso da 0
    2: 0.2,  # Esempio, devi calcolare il valore corretto
    3: 0.2,  # Esempio, devi calcolare il valore corretto
    4: 0.2,  # Esempio, devi calcolare il valore corretto
    5: 0.2  # Esempio, devi calcolare il valore corretto
}

TASSO_DI_SERVIZIO3 = 0.6  # Tasso di servizio del server 3
NUMERO_DI_SERVER1 = 2  # Numero di server del tipo 1
NUMERO_DI_SERVER2 = 3  # Numero di server del tipo 2
