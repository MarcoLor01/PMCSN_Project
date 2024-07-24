import numpy as np

# Costanti per la simulazione del sistema
START = 0.0  # initial time */
STOP = 7 * 1440.0  # terminal time */

#True = Batch( infinite )  False = Base( Finite )
MODALITY = False

#STOP = 20.0
INFINITY = float(100.0 * STOP)  # must be much larger than STOP  */

#Triage
TASSO_DI_INGRESSO = 0.092163242  # ingressi (arrivals per unit time)
NUMERO_DI_SERVER_TRIAGE = 1
MEDIA_SERVIZIO_TRIAGE = 5.5
UPPER_BOUND_TRIAGE = 7
LOWER_BOUND_TRIAGE = 2
DEVIAZIONE_STANDARD_TRIAGE = 1.5

#Queue
NUMERO_DI_SERVER_QUEUE = 4
MEDIA_TASSO_DI_SERVIZIO_QUEUE = 16
TEMPO_LIMITE = 420
UPPER_BOUND_QUEUE = 27
LOWER_BOUND_QUEUE = 10
DEVIAZIONE_STANDARD_QUEUE = 4

# Esami
NUMERO_DI_SERVER_ECG = 2
MEDIA_DI_SERVIZIO_ECG = 5
UPPER_BOUND_ECG = 9
LOWER_BOUND_ECG = 3.5
DEVIAZIONE_STANDARD_ECG = 1.5

NUMERO_DI_SERVER_EMOCROMO = 1
MEDIA_DI_SERVIZIO_EMOCROMO = 5
UPPER_BOUND_EMOCROMO = 8
LOWER_BOUND_EMOCROMO = 3.5
DEVIAZIONE_STANDARD_EMOCROMO = 1

NUMERO_DI_SERVER_ECOGRAFIA = 2
MEDIA_DI_SERVIZIO_ECOGRAFIA = 15
UPPER_BOUND_ECOGRAFIA = 20
LOWER_BOUND_ECOGRAFIA = 10
DEVIAZIONE_STANDARD_ECOGRAFIA = 2

NUMERO_DI_SERVER_RADIOGRAFIA = 2
MEDIA_DI_SERVIZIO_RADIOGRAFIA = 25
UPPER_BOUND_RADIOGRAFIA = 33
LOWER_BOUND_RADIOGRAFIA = 20
DEVIAZIONE_STANDARD_RADIOGRAFIA = 5

NUMERO_DI_SERVER_TAC = 1
MEDIA_DI_SERVIZIO_TAC = 25
UPPER_BOUND_TAC = 38
LOWER_BOUND_TAC = 17
DEVIAZIONE_STANDARD_TAC = 4

NUMERO_DI_SERVER_ALTRI_ESAMI = 3
MEDIA_DI_SERVIZIO_ALTRI_ESAMI = 35
UPPER_BOUND_ALTRI_ESAMI = 40
LOWER_BOUND_ALTRI_ESAMI = 20
DEVIAZIONE_STANDARD_ALTRI_ESAMI = 5

UPPER_BOUND_ANALISI = [UPPER_BOUND_ECG, UPPER_BOUND_EMOCROMO, UPPER_BOUND_TAC, UPPER_BOUND_RADIOGRAFIA,
                       UPPER_BOUND_ECOGRAFIA, UPPER_BOUND_ALTRI_ESAMI]
LOWER_BOUND_ANALISI = [LOWER_BOUND_ECG, LOWER_BOUND_EMOCROMO, LOWER_BOUND_TAC, LOWER_BOUND_RADIOGRAFIA,
                       LOWER_BOUND_ECOGRAFIA, LOWER_BOUND_ALTRI_ESAMI]
DEVIAZIONE_STANDARD_ANALISI = [DEVIAZIONE_STANDARD_ECG, DEVIAZIONE_STANDARD_EMOCROMO, DEVIAZIONE_STANDARD_TAC,
                               DEVIAZIONE_STANDARD_RADIOGRAFIA, DEVIAZIONE_STANDARD_ECOGRAFIA,
                               DEVIAZIONE_STANDARD_ALTRI_ESAMI]

