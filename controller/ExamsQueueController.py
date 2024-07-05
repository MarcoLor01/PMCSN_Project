from utility.Rngs import random, selectStream
from utility.Utils import *
from utility.Parameters import *
from model.Job import *
from utility.ArrivalService import *
import logging

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


def pass_to_analisi():
    selectStream(6)
    num_analisi = determina_numero_analisi()
    selectStream(7)
    analisi_da_fare = determina_analisi_da_fare(num_analisi)
    return analisi_da_fare


def determina_numero_analisi():
    # Probabilità cumulative per il numero di analisi da fare (0-6)
    num_analisi = [0, 1, 2, 3, 4, 5, 6]
    cumulative_probabilities = [0.1, 0.2, 0.35, 0.5, 0.7, 0.9, 1.0]  # Esempio di probabilità cumulative

    rand_num = random.random()
    for num, cum_prob in zip(num_analisi, cumulative_probabilities):
        if rand_num < cum_prob:
            return num


def determina_analisi_da_fare(num_analisi):
    # Le analisi disponibili
    analisi = ['ECG', 'EMOCROMO', 'TAC', 'RADIOGRAFIA', 'ECOGRAFIA', 'ALTRO']
    # Probabilità cumulative per ciascuna analisi
    cumulative_probabilities = [0.2, 0.4, 0.6, 0.75, 0.9, 1.0]  # Esempio di probabilità cumulative

    analisi_da_fare = []
    while len(analisi_da_fare) < num_analisi:
        rand_num = random.random()
        for analisi_singola, cum_prob in zip(analisi, cumulative_probabilities):
            if rand_num < cum_prob:
                if analisi_singola not in analisi_da_fare:
                    analisi_da_fare.append(analisi_singola)
                    break
    return analisi_da_fare


def main():
    print(pass_to_analisi())


if __name__ == "__main__":
    main()