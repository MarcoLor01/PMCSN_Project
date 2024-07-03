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

area_queue = Track(NUMERO_DI_SERVER_QUEUE, len(queue))
t_queue = Time(NUMERO_DI_SERVER_QUEUE)
index_queue = 0
number_queue = 0
servers_busy_queue = [False] * 5  # track busy/free status of servers


def pass_to_queue(job: Job, queue_):
    if job.get_codice() == 1:
        queue_[job.get_codice() - 1].append(job)
    else:
        queue_[job.get_codice() + 1].append(job)


def printt():
    for i in queue:
        print("Lunghezza coda: ", len(i))


def init_queue(t_queue):
    t_queue.arrival = INFINITY + 1
    t_queue.current = START  # set the clock
    for i in range(NUMERO_DI_SERVER_QUEUE):
        t_queue.completion[i] = INFINITY + 1  # the first event can't be a completion */
        area_queue.service[i] = 0
    for i in range(len(queue)):
        area_queue.wait_time[i] = 0
        area_queue.jobs_complete_color[i] = 0
    area_queue.node = 0
    area_queue.queue = 0


def pre_process_queue(t, area, number, server_busy):
    t.min_completion, t.server_index = min_time_completion(
        t.completion + [INFINITY])  # include INFINITY for queue check
    t.next = t.min_completion  # next event time
    if number > 0:
        area.node += (t.next - t.current) * number
        area.queue += (t.next - t.current) * (number - sum(server_busy))
        for i in range(NUMERO_DI_SERVER_QUEUE):
            area.service[i] = area.service[i] + (t.next - t.current) * \
                              server_busy[i]
    t.current = t.next  # advance the clock


def arrival_queue(t, servers_busy, queue):
    for i in range(NUMERO_DI_SERVER_QUEUE):
        if not servers_busy[i]:  # check if server is free
            job_to_serve = get_next_job_to_serve(queue)
            if job_to_serve:
                servers_busy[i] = True
                temp=GetServiceQueue()
                t.completion[i] = t.current + temp
                break



def completition_queue(t, server_busy, queue, area):
    return 0

    #return job_to_serve
