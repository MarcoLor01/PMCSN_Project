from utility.Rngs import random, selectStream
from utility.Utils import *
from utility.Parameters import *
from model.Job import *
from utility.ArrivalService import *
import logging
from controller.ExamsQueueController import analisi_disponibili
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
MEDIA_DI_SERVIZIO_ANALISI = [MEDIA_DI_SERVIZIO_ECG, MEDIA_DI_SERVIZIO_EMOCROMO, MEDIA_DI_SERVIZIO_TAC,
                             MEDIA_DI_SERVIZIO_RADIOGRAFIA, MEDIA_DI_SERVIZIO_ECOGRAFIA, MEDIA_DI_SERVIZIO_ALTRI_ESAMI]


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


def init_esame(t1: Time, area1: Track, queue1: list, num):
    t1.arrival = -1
    t1.current = START  # set the clock
    for i in range(num):
        t1.completion[i] = INFINITY + 1  # the first event can't be a completion */
        area1.service[i] = 0
    for i in range(len(queue1)):
        area1.wait_time[i] = 0
        area1.jobs_complete_color[i] = 0
    area1.node = 0
    area1.queue1 = 0


def init_analisi(t1, area1, queue1):
    for i in range(len(t1)):
        init_esame(t1[i], area1[i], queue1[i], NUMERO_SERVER_ANALISI[i])


def pre_process_esame(t3, area3, number3, server_busy3, num3):
    #print("tlen: ", len(t3.completion))
    t3.min_completion, t3.server_index = min_time_completion(
        t3.completion + [INFINITY])  # include INFINITY for queue check

    #t3.next = t3.min_completion
    t3.next = minimum(t3.min_completion, t3.arrival)  # next event time
    print ("MIN Comp: ", t3.min_completion, "COMP:", t3.completion, "T_NEXT:",t3.next)

    if number3 > 0:
        area3.node += (t3.next - t3.current) * number3
        area3.queue += (t3.next - t3.current) * (number3 - sum(server_busy3))
        for i in range(num3):
            area3.service[i] = area3.service[i] + (t3.next - t3.current) * \
                               server_busy3[i]
    t3.current = t3.next  # advance the clock


def pre_process_analisi(t2, area2, number2, server_busy2):
    for i in range(len(t2)):
        pre_process_esame(t2[i], area2[i], number2[i], server_busy2[i], NUMERO_SERVER_ANALISI[i])


def pass_to_analisi(job: Job, queue1, t1):
    analisi = get_next_analisi(job)
    analisi_da_fare = job.get_lista_analisi()[analisi]
    #print("analisi_da_fare:", analisi_da_fare)
    analisi, posto_analisi = switch(analisi_da_fare, job)
    #print("posto_analisi:", analisi,"posto", posto_analisi)
    t_Analisi[analisi].arrival = t1.current
    t_Analisi[analisi].arrival = check_arrival(t1.arrival + STOP)  # DA RIVEDERE
    arrival_analisi(t_Analisi[analisi], servers_busy_Analisi[analisi], queue1[analisi], analisi)
    return analisi


#
#    analisi_tipo, posto_analisi = switch(analisi_da_fare, job)
#    arrival_analisi(t_Analisi[analisi_tipo], servers_busy_Analisi[analisi_tipo], queue1[analisi_tipo], analisi_tipo)
#    t_Analisi[analisi_tipo].arrival = t1.current
#    t_Analisi[analisi_tipo].arrival = check_arrival(t1.arrival)
#    job.get_lista_analisi().pop(analisi)
#return analisi_tipo


def get_next_analisi(job):
    lista_analisi = job.get_lista_analisi()

    #print("Dio", lista_analisi)
    best_metric = 0
    best_index = -1

    for i in range(len(lista_analisi)):
        metric = calculate_metrics_on_analisi(lista_analisi[i])
        #print ("M",metric,"B",best_metric)
        if metric > best_metric:
            best_metric = metric
            best_index = i

    return best_index


def calculate_metrics_on_analisi(analisi):
    i = analisi_disponibili.index(analisi)
    if NUMERO_SERVER_ANALISI[i] - number_Analisi[i] > 0:
        return INFINITY
    else:
        return NUMERO_SERVER_ANALISI[i] / (number_Analisi[i] * MEDIA_DI_SERVIZIO_ANALISI[i])


def switch(analisi_da_fare, job: Job):
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

    queue_Analisi[num_coda][queue_posto].append(job)
    return num_coda, queue_posto


def arrival_analisi(t, servers_busy, queue_1, analisi):
    if t.arrival > STOP:
        t.last = t.current
        t.arrival = INFINITY

    for i in range(NUMERO_SERVER_ANALISI[analisi]):
        if not servers_busy[i]:  # check if server is free
            job_to_serve = get_next_job_to_serve(queue_1)
            if job_to_serve:
                servers_busy[i] = True
                server_Analisi[analisi][i] = job_to_serve
                #print("Assegnazione server del job", job_to_serve.get_id())
                #print("Analisi", analisi)
                t.completion[i] = t.current + GetServiceAnalisi(analisi, MEDIA_DI_SERVIZIO_ANALISI[analisi])
                break


def completion_analisi(t1, server_busy1, queue_q1, area1, index1):
    server_busy1[t1.server_index] = False
    t1.completion[t1.server_index] = INFINITY
    area1.jobs_completed[t1.server_index] += 1
    job_completed = server_Analisi[index1][t1.server_index]
    job_to_serve = get_next_job_to_serve(queue_q1)
    if job_to_serve:
        server_busy1[t1.server_index] = True
        server_Analisi[index1][t1.server_index] = job_to_serve
        t1.completion[t1.server_index] = t1.current + GetServiceAnalisi(index1, MEDIA_DI_SERVIZIO_ANALISI[index1])

    if job_completed:
        if job_completed.get_codice() == 1:
            area1.wait_time[job_completed.get_codice() - 1] += (t1.current - job_completed.get_arrival_temp())
            area1.jobs_complete_color[job_completed.get_codice() - 1] += 1
        else:
            area1.wait_time[1] += (t1.current - job_completed.get_arrival_temp())
            area1.jobs_complete_color[1] += 1
    else:
        logger.error("Job set to null")
    t1.last = t1.current

    return job_completed


def analisi_data(area_a, t_a, queue_a):
    logger.info("ECG = 1, EMOCROMO = 2, TAC = 3, RADIOGRAFIA = 4, ECOGRAFIA = 5, ALTRO = 6")
    for i in range(len(area_a)):
        single_analisi_data(area_a[i], t_a[i], queue_a[i], i)


def probabilita_analisi(volte_analisi):
    selectStream(25)
    if volte_analisi <= 1:
        return True
    elif volte_analisi == 2:
        return random() <= 0.2  # 20% di probabilità
    elif volte_analisi == 3:
        return False  # 5% di probabilità
    else:
        return False  # 1% di probabilità


#TODO
#0 - IMOSTARE I COMPLETAMENTI IN BASE ALL'ISTANTE CORRETTO PROXEVENT - IN ARRIVAL QUEUE
#1 - Cambiare gestione tempo intera simulazione allineando tutti gli eventi, capire prima l'evento ed eseguirlo non piu
# in modo sequenziale. Minimo tra i min completition
#2 - Problema con job che si perdono
#3 - Errore di remove sulle analisi, causato da inserimento in coda sbagliata?
#4 - Tutti i tempi di servizio
#
#5 - Scheduling adattivo per migliorare se aspetti troppo ti mando
#6 - Sensibilizzazione della popolazione
#7 - Ridurre il numero di analisi

def single_analisi_data(area, t, queue_first, index):
    logger.info(f"STATS FOR ANALISI: {index:.2f}")

    #print("T.LAST: ", t.last, "COMPLETED: ", area.jobs_completed, "AREANODE: ", area.node, "AREAQUEUE: ", area.queue, "AREA SERVICE: ", area.service)

    logger.info(
        f"Average interarrival time: {t.last / sum(area.jobs_completed) if sum(area.jobs_completed) > 0 else 0 :.2f}")
    logger.info(f"Average wait: {area.node / sum(area.jobs_completed) if sum(area.jobs_completed) > 0 else 0 :.2f}")
    logger.info(f"Average delay: {area.queue / sum(area.jobs_completed) if sum(area.jobs_completed) > 0 else 0 :.2f}")
    logger.info(
        f"Average service time: {sum(area.service) / sum(area.jobs_completed) if sum(area.jobs_completed) > 0 else 0 :.2f}")
    logger.info(f"Average number_triage in the node: {area.node / t.last:.8f}")
    logger.info(f"Average number_triage in the queue: {area.queue / t.last:.8f}")

    for i in range(NUMERO_SERVER_ANALISI[index]):
        utilization = area.service[i] / t.last if t.last > 0 else 0
        avg_service_time = area.service[i] / area.jobs_completed[i] if area.jobs_completed[i] > 0 else 0
        logger.info(f"Utilization of server {i + 1}: {utilization:.8f}")
        logger.info(f"Average service time of server {i + 1}: {avg_service_time:.2f}")
    for i in range(len(queue_first)):
        if area.jobs_complete_color[i] != 0:
            # logger.info(f"Waiting time for color {i + 1}: {area.wait_time[i]}")
            # logger.info(f"job for color {i + 1}: {area.jobs_complete_color[i]}")
            logger.info(f"Attesa media {i + 1}: {area.wait_time[i] / area.jobs_complete_color[i]}")
