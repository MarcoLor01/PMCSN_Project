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
job_att_inter_triage = 0
servers_busy_triage = [False] * NUMERO_DI_SERVER_TRIAGE  # track busy/free status of servers
server_triage = [Job] * NUMERO_DI_SERVER_TRIAGE


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


def pre_process_triage(t, area, number, server_busy):
    t.min_completion, t.server_index = min_time_completion(
        t.completion + [INFINITY])  # include INFINITY for queue check
    t.next = minimum(t.arrival, t.min_completion)  # next event time

    if number > 0 and t.last != t.next:
        if t.last>t.next:
            print("T_next", t.next, "T_last", t.last)
        area.node += (t.next - t.current) * number
        area.queue += (t.next - t.current) * (number - sum(server_busy) - job_att_inter_triage)
        for i in range(NUMERO_DI_SERVER_TRIAGE):
            if server_busy[i]:
                area.service[i] = area.service[i] + (t.next - t.current)
        if job_att_inter_triage:
            area.service_preemptive = area.service_preemptive + job_att_inter_triage * (t.next - t.current)
    t.current = t.next  # advance the clock
    if t.next < INFINITY:
        t.last = t.next


def arrival_triage(t, servers_busy, queue_t):
    global job_att_inter_triage
    full = True
    index = -1
    codice = -1
    if t.arrival > STOP:
        t.arrival = INFINITY

    for i in range(NUMERO_DI_SERVER_TRIAGE):
        if not servers_busy[i]:  # check if server is free
            full = False
            job_to_serve = get_next_job_to_serve(queue_t)
            if job_to_serve:
                server_triage[i] = job_to_serve
                servers_busy[i] = True
                if job_to_serve.get_tempo_rimanente() == 0:
                    t.completion[i] = t.current + GetServiceTriage()
                    job_to_serve.set_time_triage(t.current)
                else:
                    job_att_inter_triage = job_att_inter_triage - 1
                    t.completion[i] = t.current + job_to_serve.get_tempo_rimanente()
                break

    # preemption
    if full and (len(queue_t[0])) > 0:
        job_to_serve = get_next_job_to_serve(queue_t)
        for i in range(NUMERO_DI_SERVER_TRIAGE):
            temp = server_triage[i].get_codice()
            if temp > codice:
                codice = temp
                index = i

        job_interrotto = server_triage[index]

        if job_interrotto.get_codice() == 1 or t.completion[index] == t.current:
            queue_t[job_to_serve.get_codice() - 1].insert(0, job_to_serve)

        else:
            job_to_serve.set_time_triage(t.current)
            job_att_inter_triage = job_att_inter_triage + 1
            job_interrotto.set_tempo_rimanente(t.completion[index] - t.current)
            server_triage[index] = job_to_serve
            queue_t[job_interrotto.get_codice() - 1].insert(0, job_interrotto)
            t.completion[index] = t.current + GetServiceTriage()



def completion_triage(t, server_busy, queue_t, area):
    global job_att_inter_triage
    server_busy[t.server_index] = False
    t.completion[t.server_index] = INFINITY
    area.jobs_completed[t.server_index] += 1
    job_completed = server_triage[t.server_index]
    job_to_serve = get_next_job_to_serve(queue_t)

    if job_to_serve:
        server_triage[t.server_index] = job_to_serve
        server_busy[t.server_index] = True
        if job_to_serve.get_tempo_rimanente() == 0:
            t.completion[t.server_index] = t.current + GetServiceTriage()
            job_to_serve.set_time_triage(t.current)
        else:
            t.completion[t.server_index] = t.current + job_to_serve.get_tempo_rimanente()
            job_att_inter_triage = job_att_inter_triage - 1

    if job_completed is Job or job_completed:
        area.wait_time[job_completed.get_codice() - 1] += t.current - job_completed.get_id()
        area.jobs_complete_color[job_completed.get_codice() - 1] += 1
        area.delay_time[job_completed.get_codice() - 1] += job_completed.get_time_triage() - job_completed.get_id()

    #print("Completato job con colore: ", job_completed.get_codice(), "e codice: ", job_completed.get_id())
    return job_completed


def triage_data(area, t, queue_triage):
    logger.info("STATS FOR TRIAGE")
    logger.info(f"Average interarrival time: {t.last / sum(area.jobs_completed):.2f}")
    logger.info(f"Average wait: {area.node / sum(area.jobs_completed):.2f}")
    logger.info(f"Average delay: {area.queue / sum(area.jobs_completed):.2f}")
    logger.info(f"Average delay NOW: {sum(area.delay_time) / sum(area.jobs_completed):.2f}")
    logger.info(f"Average service time: {(sum(area.service) + area.service_preemptive) / sum(area.jobs_completed):.2f}")
    logger.info(f"Average number_triage in the node: {area.node / t.last:.2f}")
    logger.info(f"Average number_triage in the queue: {area.queue / t.last:.2f}")
    for i in range(NUMERO_DI_SERVER_TRIAGE):
        utilization = area.service[i] / t.last if t.last > 0 else 0
        logger.info(f"Utilization of server {i + 1}: {utilization:.2f}")

    for i in range(len(queue_triage)):
        if area.jobs_complete_color[i] != 0:
            # logger.info(f"Waiting time for color {i + 1}: {area.wait_time[i]}")
            # logger.info(f"job for color {i + 1}: {area.jobs_complete_color[i]}")
            logger.info(
                f"Tempo di risposta medio {i + 1}: {area.wait_time[i] / area.jobs_complete_color[i]:.10f}")
            logger.info(
                f"Tempo di attesa medio {i + 1}: {area.delay_time[i] / area.jobs_complete_color[i]:.10f}")
