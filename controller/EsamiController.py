from utility.Rngs import random, selectStream
from utility.Utils import *
from utility.Parameters import *
from model.Job import *
from utility.ArrivalService import *
import logging
from controller.EcgController import number_Ecg, index_Ecg, queue_Ecg, area_Ecg, t_Ecg, servers_busy_Ecg, server_Ecg
from controller.EmocromoController import number_Emocromo, index_Emocromo, queue_Emocromo, area_Emocromo, t_Emocromo, \
    servers_busy_Emocromo, server_Emocromo
from controller.TacController import number_Tac, index_Tac, queue_Tac, area_Tac, t_Tac, servers_busy_Tac, server_Tac
from controller.RadiografiaController import number_Radiografia, index_Radiografia, queue_Radiografia, area_Radiografia, \
    t_Radiografia, servers_busy_Radiografia, server_Radiografia
from controller.EcografiaController import number_Ecografia, index_Ecografia, queue_Ecografia, area_Ecografia, \
    t_Ecografia, servers_busy_Ecografia, server_Ecografia
from controller.AltriEsamiController import number_altriEsami, index_altriEsami, queue_altriEsami, area_altriEsami, \
    t_altriEsami, servers_busy_altriEsami, server_altriEsami

#ECG = 1, EMOCROMO = 2, TAC = 3, RADIOGRAFIA = 4, ECOGRAFIA = 5, ALTRO = 6

# Configurazione del logger
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

number_Analisi = [number_Ecg, number_Emocromo, number_Tac, number_Radiografia, number_Ecografia, number_altriEsami]
index_Analisi = [index_Ecg, index_Emocromo, index_Tac, index_Radiografia, index_Ecografia, index_altriEsami]
queue_Analisi = [queue_Ecg, queue_Emocromo, queue_Tac, queue_Radiografia, queue_Ecografia, queue_altriEsami]
servers_busy_Analisi = [servers_busy_Ecg, servers_busy_Emocromo, servers_busy_Tac, servers_busy_Radiografia,
                        servers_busy_Ecografia, servers_busy_altriEsami]
t_Analisi = [t_Ecg, t_Emocromo, t_Tac, t_Radiografia, t_Ecografia, t_altriEsami]
area_Analisi = [area_Ecg, area_Emocromo, area_Tac, area_Radiografia, area_Ecografia, area_altriEsami]
server_Analisi = [server_Ecg, server_Emocromo, server_Tac, server_Radiografia, server_Ecografia, server_altriEsami]

NUMERO_SERVER_ANALISI = [NUMERO_DI_SERVER_ECG, NUMERO_DI_SERVER_EMOCROMO, NUMERO_DI_SERVER_TAC,
                         NUMERO_DI_SERVER_RADIOGRAFIA, NUMERO_DI_SERVER_ECOGRAFIA, NUMERO_DI_SERVER_ALTRI_ESAMI]


def assign_esami():
    # Lista dei codici corrispondenti
    # ECG = 1, EMOCROMO = 2, TAC = 3, RADIOGRAFIA = 4, ECOGRAFIA = 5, ALTRO = 6
    esami = [1, 2, 3, 4, 5, 6]
    # Probabilità cumulative corrispondenti
    cumulative_probabilities = [0.063, 0.259, 0.350, 0.642, 0.948, 1.0]  # Probabilità cumulative

    rand_num = random()
    # Determinare il codice basato sul numero casuale
    for esame, cum_prob in zip(esami, cumulative_probabilities):
        if rand_num < cum_prob:
            return esame


def init_esame(t: Time, area: Track, queue: list, num):
    t.arrival = -1
    t.current = START  # set the clock
    for i in range(num):
        t.completion[i] = INFINITY + 1  # the first event can't be a completion */
        area.service[i] = 0
    for i in range(len(queue)):
        area.wait_time[i] = 0
        area.jobs_complete_color[i] = 0
    area.node = 0
    area.queue = 0


def init_analisi(t, area, queue):
    for i in range(len(t)):
        init_esame(t[i], area[i], queue[i], NUMERO_SERVER_ANALISI[i])


def pre_process_esame(t, area, number, server_busy, num):
    t.min_completion, t.server_index = min_time_completion(
        t.completion + [INFINITY])  # include INFINITY for queue check
    t.next = minimum(t.min_completion, t.arrival)  # next event time
    if number > 0:
        area.node += (t.next - t.current) * number
        area.queue += (t.next - t.current) * (number - sum(server_busy))
        for i in range(num):
            area.service[i] = area.service[i] + (t.next - t.current) * \
                              server_busy[i]
    t.current = t.next  # advance the clock


def pre_process_analisi(t, area, number, server_busy):
    for i in range(len(t)):
        pre_process_esame(t[i], area[i], number[i], server_busy[i], NUMERO_SERVER_ANALISI[i])


def pass_to_analisi(job: Job, queue_, t):
    analisi_da_fare = job.get_lista_analisi()[0]
    analisi, posto_analisi = switch(analisi_da_fare, job)
    arrival_analisi(t_Analisi[analisi], servers_busy_Analisi[analisi], queue_[analisi], analisi)
    t_Analisi[analisi].arrival = t.current


def switch(analisi_da_fare, job: Job):
    queue_posto = -1
    num_coda = -1

    if job.get_codice() == 1:
        queue_posto = 0
    else:
        queue_posto = 1

    if analisi_da_fare == "ECG":
        num_coda = 0
    elif analisi_da_fare == "Emocromo":
        num_coda = 1
    elif analisi_da_fare == "Tac":
        num_coda = 2
    elif analisi_da_fare == "Radiografia":
        num_coda = 3
    elif analisi_da_fare == "Ecografia":
        num_coda = 4
    elif analisi_da_fare == "Altro":
        num_coda = 5
    else:
        logger.error("Analisi non presente")

    if queue_posto != -1 and num_coda != -1:
        queue_Analisi[num_coda][queue_posto].append(job)
    else:
        logger.error("Errore nell'aggiornamento")

    return num_coda, queue_posto


def arrival_analisi(t, servers_busy, queue_q, analisi):
    if t.arrival > STOP:
        t.last = t.current
        t.arrival = INFINITY

    for i in range(NUMERO_SERVER_ANALISI[analisi]):
        if not servers_busy[i]:  # check if server is free
            job_to_serve = get_next_job_to_serve(queue_q)
            if job_to_serve:
                servers_busy[i] = True
                server_Analisi[analisi][i] = job_to_serve
                t.completion[i] = t.current + GetServiceQueue()
                break





##    print(analisi_da_fare, " Codice: ", job.get_codice())
##    for i in range(len(queue_Analisi)):
##        for j in range(len(queue_Analisi[i])):
##            print("CODE: i=",i,"j=",j,"   ", len(queue_Analisi[i][j]))
# ECG = 1, EMOCROMO = 2, TAC = 3, RADIOGRAFIA = 4, ECOGRAFIA = 5, ALTRO = 6

#TODO
#1 - Aggiungere alla classe job gli esami da fare e gli esami fatti
#2 - Creare una funzione che terminato l'esame mette il job in coda per l'esame con coda minore
#3 - Iniziare a ragionare sui preemptive, come li gestiamo?
