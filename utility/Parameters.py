import numpy as np

# Costanti per la simulazione del sistema
START = 0.0  # initial time */
STOP = 200000.0  # terminal time */

INFINITY = float(100.0 * STOP)  # must be much larger than STOP  */

#Triage
TASSO_DI_INGRESSO = 0.092163242  # ingressi (arrivals per unit time)
NUMERO_DI_SERVER_TRIAGE = 1
SX_SERVIZIO_TRIAGE = 4
DX_SERVIZIO_TRIAGE = 7

#Queue
NUMERO_DI_SERVER_QUEUE = 4
MEDIA_TASSO_DI_SERVIZIO_QUEUE = 0.8  # Tasso di servizio del server 2


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

TASSO_DI_SERVIZIO = 0.8  # Tasso di servizio del server 2
TASSO_DI_SERVIZIO3 = 0.6  # Tasso di servizio del server 3
NUMERO_DI_SERVER1 = 2  # Numero di server del tipo 1
NUMERO_DI_SERVER2 = 3  # Numero di server del tipo 2
