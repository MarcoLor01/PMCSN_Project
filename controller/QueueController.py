from utility.Rngs import random, selectStream
from utility.Utils import *
from utility.Parameters import *
from model.Job import *
from utility.ArrivalService import *
import logging

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
servers_busy_queue = [False] * 5  # track busy/free status of servers


def pass_to_queue(job: Job, queue_, t):
    #global number_queue
    #number_queue += 1
    if job.get_codice() == 1:
        queue_[job.get_codice() - 1].append(job)
    else:
        queue_[job.get_codice() + 1].append(job)
    arrival_queue(t_queue, servers_busy_queue, queue_)
    t_queue.arrival = t.current


def printt():
    for i in queue:
        print("Lunghezza coda: ", len(i))


def init_queue():
    t_queue.arrival = -1
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
    for i in range(NUMERO_DI_SERVER_QUEUE):
        if not servers_busy[i]:  # check if server is free
            job_to_serve = get_next_job_to_serve(queue_q)
            if job_to_serve:
                servers_busy[i] = True
                server_queue[i] = job_to_serve
                t.completion[i] = t.current + GetServiceQueue()
                break


def completion_queue(t, server_busy, queue_q, area):
    server_busy[t.server_index] = False
    t.completion[t.server_index] = INFINITY
    area.jobs_completed[t.server_index] += 1
    job_completed = server_queue[t.server_index]
    job_to_serve = get_next_job_to_serve(queue_q)

    if job_to_serve:
        server_busy[t.server_index] = True
        server_queue[t.server_index] = job_to_serve
        t.completion[t.server_index] = t.current + GetServiceQueue()
        area.wait_time[
            job_to_serve.get_codice() - 1] += t.current - job_to_serve.get_arrival_temp()
        area.jobs_complete_color[job_to_serve.get_codice() - 1] += 1
    return job_completed
