from utility.Rngs import random
from utility.ArrivalService import *
import logging
from model.Job import *

# Configurazione del logger
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

# ECG = 1, EMOCROMO = 2, TAC = 3, RADIOGRAFIA = 4, ECOGRAFIA = 5, ALTRO = 6
NUMERO_DI_SERVER_ANALISI = [2, 2, 2, 2, 2, 2]
NUMERO_DI_ANALISI = 6

server_list = [[] for _ in range(NUMERO_DI_ANALISI)]

for i in range(len(NUMERO_DI_SERVER_ANALISI)):
    server_list[i] = [[Job] for _ in range(NUMERO_DI_SERVER_ANALISI[i])]

# Inizializzazione delle code rosse
queueRed_a = [[] for _ in range(NUMERO_DI_ANALISI)]

# Inizializzazione delle code non rosse
queueNotRed_a = [[] for _ in range(NUMERO_DI_ANALISI)]

# Creazione della lista unica contenente le due code
queue_analisi = [queueRed_a, queueNotRed_a]


def get_analisi():
    num_analisi = determina_numero_analisi()
    analisi_da_fare = esegui_analisi(num_analisi)
    return analisi_da_fare


def determina_numero_analisi():
    # Probabilità cumulative per il numero di analisi da fare (0-6)
    selectStream(5)
    num_analisi = [0, 1, 2, 3, 4, 5, 6]
    cumulative_probabilities = [0.0, 0.089, 0.389, 0.889, 0.989, 0.999, 1.0]
    rand_num = random()
    for num, cum_prob in zip(num_analisi, cumulative_probabilities):
        if rand_num <= cum_prob:
            return num


# Counter({3: 499813, 2: 299887, 4: 99999, 1: 89192, 5: 10092, 6: 1017})

# Frequenze desiderate per ciascun tipo di analisi per ogni numero di analisi
frequenze_assolute = {
    1: {'ECG': 0, 'Ecografia': 0, 'Emocromo': 40, 'Radiografia': 30, 'Tac': 0, 'Altro': 30},
    2: {'ECG': 0, 'Ecografia': 20, 'Emocromo': 90, 'Radiografia': 42, 'Tac': 6, 'Altro': 42},
    3: {'ECG': 90, 'Ecografia': 20, 'Emocromo': 99, 'Radiografia': 40, 'Tac': 6, 'Altro': 45},
    4: {'ECG': 105, 'Ecografia': 32, 'Emocromo': 112, 'Radiografia': 63, 'Tac': 20, 'Altro': 68},
    5: {'ECG': 110, 'Ecografia': 50, 'Emocromo': 130, 'Radiografia': 80, 'Tac': 25, 'Altro': 105},
    6: {'ECG': 120, 'Ecografia': 57, 'Emocromo': 143, 'Radiografia': 95, 'Tac': 30, 'Altro': 155}
}

analisi_disponibili = ['ECG', 'Emocromo', 'Tac', 'Radiografia', 'Ecografia', 'Altro']


def scegli_analisi(numero_analisi):
    selectStream(6)
    analisi_frequenze = frequenze_assolute[numero_analisi]
    totale_frequenze = sum(analisi_frequenze.values())
    cumulative_prob = {}
    cumulative = 0
    for nome in analisi_disponibili:
        cumulative += analisi_frequenze[nome] / totale_frequenze
        cumulative_prob[nome] = cumulative

    analisi_da_fare = []
    for _ in range(numero_analisi):
        rand_num = random()
        for nome in analisi_disponibili:
            if rand_num < cumulative_prob[nome]:
                analisi_da_fare.append(nome)
                break

    return analisi_da_fare


def esegui_analisi(numero_analisi):

    return scegli_analisi(numero_analisi)
