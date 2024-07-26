from model.Job import Job
from utility.Rngs import random
from utility.Utils import *
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

# ECG = 1, EMOCROMO = 2, TAC = 3, RADIOGRAFIA = 4, ECOGRAFIA = 5, ALTRO = 6

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
    esami = [1, 2, 3, 4, 5, 6]
    cumulative_probabilities = [0.063, 0.259, 0.350, 0.642, 0.948, 1.0]
    rand_num = random()
    for esame, cum_prob in zip(esami, cumulative_probabilities):
        if rand_num < cum_prob:
            return esame


def init_esame(t1, area1, queue1, num):
    t1.arrival = START
    t1.current = START
    for i in range(num):
        t1.completion[i] = INFINITY
        area1.service[i] = 0
    for i in range(len(queue1)):
        area1.wait_time[i] = 0
        area1.jobs_complete_color[i] = 0
    area1.node = 0
    area1.queue = 0


def init_analisi(t1, area1, queue1):
    for i in range(len(t1)):
        init_esame(t1[i], area1[i], queue1[i], NUMERO_SERVER_ANALISI[i])


def pre_process_esame(t3, area3, number3, server_busy3, num3):
    t3.min_completion, t3.server_index = min_time_completion(t3.completion + [INFINITY])
    t3.next = t3.min_completion
    if number3 > 0 and t3.last != t3.next:
        area3.node += (t3.next - t3.current) * number3
        area3.queue += (t3.next - t3.current) * (number3 - sum(server_busy3))
        for i in range(num3):
            if server_busy3[i]:
                area3.service[i] += (t3.next - t3.current)
    t3.current = t3.next
    if t3.next < INFINITY:
        t3.last = t3.next


def pre_process_analisi(t2, area2, number2, server_busy2):
    for i in range(len(t2)):
        pre_process_esame(t2[i], area2[i], number2[i], server_busy2[i], NUMERO_SERVER_ANALISI[i])


def pass_to_analisi(job, queue1, t1):
    analisi = get_next_analisi(job)
    analisi_da_fare = job.get_lista_analisi()[analisi]
    analisi, posto_analisi = switch(analisi_da_fare, job)
    t_Analisi[analisi].arrival = t1.last
    t_Analisi[analisi].arrival = check_arrival(t1.arrival + STOP)
    arrival_analisi(t_Analisi[analisi], servers_busy_Analisi[analisi], queue1[analisi], analisi)
    return analisi


def get_next_analisi(job):
    lista_analisi = job.get_lista_analisi()
    best_metric = 0
    best_index = -1
    for i in range(len(lista_analisi)):
        metric = calculate_metrics_on_analisi(lista_analisi[i])
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


def switch(analisi_da_fare, job):
    num_coda = -1
    queue_posto = 0 if job.get_codice() == 1 else 1
    analisi_mapping = {
        "ECG": 0,
        "Emocromo": 1,
        "Tac": 2,
        "Radiografia": 3,
        "Ecografia": 4,
        "Altro": 5
    }
    if analisi_da_fare in analisi_mapping:
        num_coda = analisi_mapping[analisi_da_fare]
    else:
        logger.error("Analisi non presente")
    queue_Analisi[num_coda][queue_posto].append(job)
    return num_coda, queue_posto


def arrival_analisi(t, servers_busy, queue_1, analisi):
    for i in range(NUMERO_SERVER_ANALISI[analisi]):
        if not servers_busy[i]:
            job_to_serve = get_next_job_to_serve(queue_1)
            if job_to_serve:
                servers_busy[i] = True
                server_Analisi[analisi][i] = job_to_serve
                t.completion[i] = t.current + GetServiceAnalisi(analisi, MEDIA_DI_SERVIZIO_ANALISI[analisi])
                job_to_serve.set_analisi_time(t.current)
                break


def completion_analisi(t1: Time, server_busy1, queue_q1, area1, index1):
    server_busy1[t1.server_index] = False
    t1.completion[t1.server_index] = INFINITY + 1
    area1.jobs_completed[t1.server_index] += 1
    job_completed = server_Analisi[index1][t1.server_index]
    job_to_serve = get_next_job_to_serve(queue_q1)
    if job_to_serve:
        server_busy1[t1.server_index] = True
        server_Analisi[index1][t1.server_index] = job_to_serve
        t1.completion[t1.server_index] = t1.current + GetServiceAnalisi(index1, MEDIA_DI_SERVIZIO_ANALISI[index1])
        job_to_serve.set_analisi_time(t1.current)
    if job_completed is Job or job_completed:
        if job_completed.get_codice() == 1:
            area1.wait_time[job_completed.get_codice() - 1] += (t1.current - job_completed.get_arrival_temp())
            area1.jobs_complete_color[job_completed.get_codice() - 1] += 1
            area1.delay_time[job_completed.get_codice() - 1] += job_completed.get_analisi_time() - job_completed.get_arrival_temp()
        else:
            area1.wait_time[1] += (t1.current - job_completed.get_arrival_temp())
            area1.jobs_complete_color[1] += 1
            area1.delay_time[1] += job_completed.get_analisi_time() - job_completed.get_arrival_temp()

    else:
        logger.error("Job set to null")
    return job_completed


def analisi_data(area_a, t_a, queue_a):
    logger.info("ECG = 1, EMOCROMO = 2, TAC = 3, RADIOGRAFIA = 4, ECOGRAFIA = 5, ALTRO = 6")
    for i in range(len(area_a)):
        single_analisi_data(area_a[i], t_a[i], queue_a[i], i)




def probability_analisi(volte_analisi):
    selectStream(7)
    if volte_analisi <= 0:
        return True
    elif volte_analisi == 1:
        return random() <= 0.5
    elif volte_analisi == 2:
        return random() <= 0.2
    elif volte_analisi == 3:
        return random() <= 0.05
    else:
        return random() <= 0.01


def single_analisi_data(area, t, queue_first, index):
    logger.info(f"STATS FOR ANALISI: {index:.0f}")
    logger.info(
        f"Average interarrival time: {t.last / sum(area.jobs_completed) if sum(area.jobs_completed) > 0 else 0:.2f}")
    logger.info(f"Average wait: {area.node / sum(area.jobs_completed) if sum(area.jobs_completed) > 0 else 0:.2f}")
    logger.info(f"Average delay: {area.queue / sum(area.jobs_completed) if sum(area.jobs_completed) > 0 else 0:.2f}")
    logger.info(
        f"Average service time: {sum(area.service) / sum(area.jobs_completed) if sum(area.jobs_completed) > 0 else 0:.2f}")
    logger.info(f"Average number_triage in the node: {area.node / t.last:.8f}")
    logger.info(f"Average number_triage in the queue: {area.queue / t.last:.8f}")
    logger.info(f"T last: {t.last:.2f}")

    for i in range(NUMERO_SERVER_ANALISI[index]):
        utilization = area.service[i] / t.last if t.last > 0 else 0
        avg_service_time = area.service[i] / area.jobs_completed[i] if area.jobs_completed[i] > 0 else 0
        logger.info(f"Utilization of server {i + 1}: {utilization:.8f}")
        logger.info(f"Average service time of server {i + 1}: {avg_service_time:.2f}")
    for i in range(len(queue_first)):
        if area.jobs_complete_color[i] != 0:
            logger.info(f"Attesa media {i + 1}: {area.wait_time[i] / area.jobs_complete_color[i]}")
            logger.info(f"Tempo di attesa medio {i + 1}: {area.delay_time[i] / area.jobs_complete_color[i]:.10f}")
