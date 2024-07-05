from utility.Rngs import random, selectStream
from utility.Utils import *
from utility.Parameters import *
from model.Job import *
from utility.ArrivalService import *
import logging
from collections import Counter

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
    selectStream(6)
    num_analisi = determina_numero_analisi()
    selectStream(7)
    analisi_da_fare = esegui_analisi(num_analisi)
    return analisi_da_fare


# PROBABILITA ANALISI
# 0 ANALISI: 0%
# 1 ANALISI: 8.9%
# 2 ANALISI: 30%
# 3 ANALISI: 50%
# 4 ANALISI: 10%
# 5 ANALISI: 1%
# 6 ANALISI: 0.1%

# --1 ANALISI--
# ECG: 0%
# Ecografia: 0%
# Emocromo: 0.4%
# Radiografia: 0.3%
# Tac: 0%
# Altro: 0.3%

# --2 ANALISI--
# Emocromo: 0.9
# ECG:
# Radiografia: 50%
# Ecografia: 20%
# Tac: 6%
# Altro: 50%

# --3 ANALISI--
# ECG: 90%
# Ecografia: 20%
# Emocromo: 99%
# Radiografia: 50%
# Tac: 6%
# Altro: 50%

# --4 ANALISI--
# ECG: 90%
# Ecografia: 20%
# Emocromo: 99%
# Radiografia: 50%
# Tac: 6%
# Altro: 50%

# --5 ANALISI--
# ECG: 90%
# Ecografia: 20%
# Emocromo: 99%
# Radiografia: 50%
# Tac: 6%
# Altro: 50%

# --6 ANALISI--
# ECG: 90%
# Ecografia: 20%
# Emocromo: 99%
# Radiografia: 50%
# Tac: 6%
# Altro: 50%

def determina_numero_analisi():
    # Probabilità cumulative per il numero di analisi da fare (0-6)
    num_analisi = [0, 1, 2, 3, 4, 5, 6]
    cumulative_probabilities = [0.0, 0.089, 0.389, 0.889, 0.989, 0.999, 1.0]
    rand_num = random()
    for num, cum_prob in zip(num_analisi, cumulative_probabilities):
        if rand_num <= cum_prob:
            return num


# Counter({3: 499813, 2: 299887, 4: 99999, 1: 89192, 5: 10092, 6: 1017})


def scegli_analisi(analisi_disponibili):
    analisi_probabilita = {
        'Tac': 0.06,
        'Ecografia': 0.20,
        'Altro': 0.50,
        'Radiografia': 0.50,
        'ECG': 9,
        'Emocromo': 9
    }

    totale_probabilita = sum(analisi_probabilita[nome] for nome in analisi_disponibili)
    cumulative_prob = {}
    cumulative = 0
    for nome in analisi_disponibili:
        cumulative += analisi_probabilita[nome] / totale_probabilita
        cumulative_prob[nome] = cumulative

    rand_num = random()

    for nome in analisi_disponibili:
        if rand_num < cumulative_prob[nome]:
            analisi_disponibili.remove(nome)
            return nome

    return None

def esegui_analisi(numero_analisi):
    analisi_disponibili = ['ECG', 'Ecografia', 'Emocromo', 'Radiografia', 'Tac', 'Altro']
    analisi_da_fare = []

    for _ in range(numero_analisi):
        if not analisi_disponibili:
            break
        analisi = scegli_analisi(analisi_disponibili)
        if analisi:
            analisi_da_fare.append(analisi)

    return analisi_da_fare

def test_esegui_analisi(num_samples=100000):
    results = []
    for _ in range(num_samples):
        analisi = esegui_analisi(2)
        results.extend(analisi)
    counter = Counter(results)