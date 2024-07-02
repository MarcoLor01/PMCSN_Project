from utility.Rngs import random, selectStream
from utility.Utils import *
from utility.Parameters import *
from model.Job import *
from utility.ArrivalService import *
import logging

# Configurazione del logger
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

queueRed = []
queueOrange = []
queueBlue = []
queueGreen = []
queueWhite = []
queue_triage = [queueRed, queueOrange, queueBlue, queueGreen,
                queueWhite]  # queue for jobs waiting to be served divided for colors
area_triage = Track(NUMERO_DI_SERVER_TRIAGE, len(queue_triage))
t_triage = Time(NUMERO_DI_SERVER_TRIAGE)
index_triage = 0
number_triage = 0
servers_busy_triage = [False] * NUMERO_DI_SERVER_TRIAGE  # track busy/free status of servers


def give_code():
    selectStream(1)
    code = assign_triage_code()
    return code


def assign_triage_code():
    # Lista dei codici corrispondenti
    # 1 ROSSO, 2 ARANCIONE, 3 BLU, 4 VERDE, 5 BIANCO
    codes = [1, 2, 3, 4, 5]
    # Probabilità cumulative corrispondenti
    cumulative_probabilities = [0.063, 0.259, 0.642, 0.948, 1.0]  # Probabilità cumulative

    rand_num = random()
    # Determinare il codice basato sul numero casuale
    for code, cum_prob in zip(codes, cumulative_probabilities):
        if rand_num < cum_prob:
            return code


def init_triage(arrival_temp):
    t_triage.arrival = arrival_temp  # schedule the first arrival
    t_triage.current = START  # set the clock
    for i in range(NUMERO_DI_SERVER_TRIAGE):
        t_triage.completion[i] = INFINITY  # the first event can't be a completion */
        area_triage.service[i] = 0
    for i in range(len(queue_triage)):
        area_triage.wait_time[i] = 0
        area_triage.jobs_complete_color[i] = 0
    area_triage.node = 0
    area_triage.queue = 0


def pre_process_triage(t,area):
    t.min_completion, t.server_index = min_time_completion(
        t.completion + [INFINITY])  # include INFINITY for queue check
    t.next = minimum(t.arrival, t.min_completion)  # next event time
    if number_triage > 0:
        area.node += (t.next - t.current) * number_triage
        area.queue += (t.next - t.current) * (number_triage - sum(servers_busy_triage))
        for i in range(NUMERO_DI_SERVER_TRIAGE):
            area.service[i] = area.service[i] + (t.next - t.current) * \
                                     servers_busy_triage[i]
    t.current = t.next  # advance the clock


def arrival_triage(t,servers_busy, queue):


    if t.arrival > STOP:
        t.last = t.current
        t.arrival = INFINITY

    for i in range(NUMERO_DI_SERVER_TRIAGE):
        if not servers_busy[i]:  # check if server is free
            job_to_serve = get_next_job_to_serve(queue)
            if job_to_serve:
                servers_busy[i] = True
                t.completion[i] = t.current + GetServiceTriage()
                break

def completition_triage(t_triage,servers_busy_triage, queue_triage, area_triage):
    servers_busy_triage[t_triage.server_index] = False
    t_triage.completion[t_triage.server_index] = INFINITY
    area_triage.jobs_completed[t_triage.server_index] += 1

    job_to_serve = get_next_job_to_serve(queue_triage)

    if job_to_serve:
        servers_busy_triage[t_triage.server_index] = True
        t_triage.completion[t_triage.server_index] = t_triage.current + GetServiceTriage()
        area_triage.wait_time[
            job_to_serve.get_codice() - 1] += t_triage.current - job_to_serve.get_arrival_temp()
        area_triage.jobs_complete_color[job_to_serve.get_codice() - 1] += 1
    return job_to_serve

def triage_data(area_triage,t_triage,queue_triage):
    logger.info(f"Average interarrival time: {t_triage.last / sum(area_triage.jobs_completed):.2f}")
    logger.info(f"Average wait: {area_triage.node / sum(area_triage.jobs_completed):.2f}")
    logger.info(f"Average delay: {area_triage.queue / sum(area_triage.jobs_completed):.2f}")
    logger.info(f"Average service time: {sum(area_triage.service) / sum(area_triage.jobs_completed):.2f}")
    logger.info(f"Average number_triage in the node: {area_triage.node / t_triage.current:.2f}")
    logger.info(f"Average number_triage in the queue: {area_triage.queue / t_triage.current:.2f}")

    for i in range(NUMERO_DI_SERVER_TRIAGE):
        utilization = area_triage.service[i] / t_triage.current if t_triage.current > 0 else 0
        avg_service_time = area_triage.service[i] / area_triage.jobs_completed[i] if area_triage.jobs_completed[
                                                                                         i] > 0 else 0

        logger.info(f"Utilization of server {i + 1}: {utilization:.2f}")
        logger.info(f"Average service time of server {i + 1}: {avg_service_time:.2f}")
    for i in range(len(queue_triage)):
        if area_triage.jobs_complete_color[i] != 0:
            # logger.info(f"Waiting time for color {i + 1}: {area_triage.wait_time[i]}")
            # logger.info(f"job for color {i + 1}: {area_triage.jobs_complete_color[i]}")
            logger.info(f"Attesa media {i + 1}: {area_triage.wait_time[i] / area_triage.jobs_complete_color[i]}")

