from utility.Rngs import random, selectStream
from utility.Utils import *
from utility.Parameters import *
from model.Job import *
from utility.ArrivalService import *
import logging

# Configurazione del logger
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

queueRed_q = []
queueOrange_q = []
queueBlue_q = []
queueGreen_q = []
queueWhite_q = []
queueReturnRed_q = []
queueReturnNotRed_q = []
queue = [queueRed_q, queueReturnRed_q, queueReturnNotRed_q, queueOrange_q, queueBlue_q, queueGreen_q, queueWhite_q]

server_queue = [Job] * NUMERO_DI_SERVER_QUEUE
area_queue = Track(NUMERO_DI_SERVER_QUEUE, len(queue))
t_queue = Time(NUMERO_DI_SERVER_QUEUE)
index_queue = 0
number_queue = 0.0
servers_busy_queue = [False] * NUMERO_DI_SERVER_QUEUE  # track busy/free status of servers


def pass_to_queue(job: Job, queue_, t):
    if job.get_codice() == 1:
        queue_[job.get_codice() - 1].append(job)
    else:
        queue_[job.get_codice() + 1].append(job)

    arrival_queue(t_queue, servers_busy_queue, queue_)
    t_queue.arrival = t.current


def return_to_queue(job: Job, queue_, t):
    if job.get_codice() == 1:
        queue_[1].append(job)
    else:
        queue_[2].append(job)

    arrival_queue(t_queue, servers_busy_queue, queue_)
    t_queue.arrival = t.current


def init_queue():

    t_queue.arrival = START
    t_queue.current = START  # set the clock
    for i in range(NUMERO_DI_SERVER_QUEUE):
        t_queue.completion[i] = INFINITY + 1  # the first event can't be a completion */
        area_queue.service[i] = 0
    for i in range(len(queue)):
        area_queue.wait_time[i] = 0
        area_queue.jobs_complete_color[i] = 0
    area_queue.node = 0
    area_queue.queue = 0


def pre_process_queue(area, number, server_busy):

    t_queue.min_completion, t_queue.server_index = min_time_completion(
        t_queue.completion + [INFINITY])  # include INFINITY for queue check
    t_queue.next = minimum(t_queue.min_completion, t_queue.arrival)  # next event time
    if number > 0:
        area.node += (t_queue.next - t_queue.current) * number
        area.queue += (t_queue.next - t_queue.current) * (number - sum(server_busy))
        for i in range(NUMERO_DI_SERVER_QUEUE):
            area.service[i] = area.service[i] + (t_queue.next - t_queue.current) * \
                              server_busy[i]

    t_queue.current = t_queue.next  # advance the clock


def arrival_queue(t, servers_busy, queue_q):
    full = True
    index = -1
    codice = -1

    if t_queue.arrival > STOP:
        t_queue.last = t_queue.current
        t_queue.arrival = INFINITY

    for i in range(NUMERO_DI_SERVER_QUEUE):
        if not servers_busy[i]:  # check if server is free
            full = False
            job_to_serve = get_next_job_to_serve(queue_q)
            if job_to_serve:
                servers_busy[i] = True
                server_queue[i] = job_to_serve
                if job_to_serve.get_tempo_rimanente() == 0:
                    t_queue.completion[i] = t.current + GetServiceQueue()
                else:
                    t_queue.completion[i] = t.current + job_to_serve.get_tempo_rimanente()
                break

    # preemption
    if full and (len(queue_q[0]) + len(queue_q[1])) > 0:
        job_to_serve = get_next_job_to_serve(queue_q)
        for i in range(NUMERO_DI_SERVER_QUEUE):
            temp = server_queue[i].get_codice()
            if temp > codice:
                codice = temp
                index = i

        job_interrotto = server_queue[index]
        if job_interrotto.get_codice() == 1 or t.completion[index] == t.current:
            coda_preemptive(queue_q, job_to_serve)
        else:
            job_interrotto.set_tempo_rimanente(t.completion[index] - t.current)
            server_queue[index] = job_to_serve
            coda_preemptive(queue_q, job_interrotto)
            t_queue.completion[index] = t_queue.current + GetServiceQueue()


def coda_preemptive(queue_q, job):
    if job.get_uscita() and job.get_codice() == 1:
        queue_q[job.get_codice()].insert(0, job)
    elif job.get_codice() == 1:
        queue_q[job.get_codice() - 1].insert(0, job)
    elif job.get_uscita():
        queue_q[2].insert(0, job)
    else:
        queue_q[job.get_codice() + 1].insert(0, job)


def completion_queue(t, server_busy, queue_q, area):
    server_busy[t.server_index] = False
    t.completion[t.server_index] = INFINITY
    area.jobs_completed[t.server_index] += 1
    job_completed = server_queue[t.server_index]
    job_to_serve = get_next_job_to_serve(queue_q)

    if job_to_serve:
        server_busy[t.server_index] = True
        server_queue[t.server_index] = job_to_serve
        if job_to_serve.get_tempo_rimanente() == 0:
            t.completion[t.server_index] = t.current + GetServiceQueue()
        else:
            t.completion[t.server_index] = t.current + job_to_serve.get_tempo_rimanente()

    if job_completed:

        if job_completed.get_uscita():
            if job_completed.get_codice() == 1:
                area.wait_time[1] += t.current - job_completed.get_arrival_temp()
                area.jobs_complete_color[1] += 1
            else:
                area.wait_time[2] += t.current - job_completed.get_arrival_temp()
                area.jobs_complete_color[2] += 1
        elif job_completed.get_codice() == 1:
            area.wait_time[job_completed.get_codice() - 1] += t.current - job_completed.get_arrival_temp()
            area.jobs_complete_color[job_completed.get_codice() - 1] += 1
        else:
            area.wait_time[job_completed.get_codice() + 1] += t.current - job_completed.get_arrival_temp()
            area.jobs_complete_color[job_completed.get_codice() + 1] += 1

    if t.arrival > STOP:
        t.last = t.current

    return job_completed


def queue_data(area, t, queue_first):
    logger.info("STATS FOR INITIAL QUEUE")
    logger.info(f"Average interarrival time: {t.last / sum(area.jobs_completed):.2f}")
    logger.info(f"Average wait: {area.node / sum(area.jobs_completed):.2f}")
    logger.info(f"Average delay: {area.queue / sum(area.jobs_completed):.2f}")
    logger.info(f"Average service time: {sum(area.service) / sum(area.jobs_completed):.2f}")
    logger.info(f"Average number_queue in the node: {area.node / t.last:.2f}")
    logger.info(f"Average number_queue in the queue: {area.queue / t.last:.2f}")

    for i in range(NUMERO_DI_SERVER_QUEUE):
        utilization = area.service[i] / t.last if t.last > 0 else 0
        avg_service_time = area.service[i] / area.jobs_completed[i] if area.jobs_completed[
                                                                           i] > 0 else 0
        logger.info(f"Utilization of server {i + 1}: {utilization:.2f}")
        logger.info(f"Average service time of server {i + 1}: {avg_service_time:.2f}")
    for i in range(len(queue_first)):
        if area.jobs_complete_color[i] != 0:
            # logger.info(f"Waiting time for color {i + 1}: {area.wait_time[i]}")
            # logger.info(f"job for color {i + 1}: {area.jobs_complete_color[i]}")
            logger.info(f"Attesa media {i + 1}: {area.wait_time[i] / area.jobs_complete_color[i]}")
