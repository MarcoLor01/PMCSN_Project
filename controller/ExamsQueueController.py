from utility.Rngs import random, selectStream
from utility.Utils import *
from utility.Parameters import *
from model.Job import *
from utility.ArrivalService import *
import logging

# Configurazione del logger
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

#ECG = 1, EMOCROMO = 2, TAC = 3, RADIOGRAFIA = 4, ECOGRAFIA = 5, ALTRO = 6
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



