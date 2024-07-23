from utility.Parameters import INFINITY, STOP, TEMPO_LIMITE


def minimum(a, c):
    # ------------------------------
    # * return the smaller of a, b
    # * ------------------------------
    # */
    if a < c:
        return a
    else:
        return c


def min_time_completion(completion_times):
    """Returns the minimum completion time and the index of the server"""
    min_completion_time = min(completion_times)
    min_index = completion_times.index(min_completion_time)
    if min_index == len(completion_times) - 1:
        min_index = 0
    return min_completion_time, min_index


def get_next_job_to_serve(list_of_queues, t=0):
    if len(list_of_queues) == 7:
        if (len(list_of_queues[0]) + len(list_of_queues[1])) <= 0:
            job = get_job_old(list_of_queues, t)
            if job:
                return job

    """Selects the next job to serve based on a priority policy"""
    for queue in list_of_queues:
        if queue:
            return queue.pop(0)  # Simple FIFO (First In, First Out) policy for each priority queue
    return None


def get_job_old(list_of_queues, t):
    """Selects the next job to serve based on a priority policy"""
    for queue in list_of_queues:
        if queue and queue[0] and (t.current - queue[0].get_id()) > TEMPO_LIMITE:
            return queue.pop(0)
    return None


def add_job_to_queue(job, queue):
    index = job.get_codice() - 1  # Utilizza getCodice per determinare l'indice della lista
    if 0 <= index < len(queue):
        queue[index].append(job)
    else:
        print(f"Index {index} is out of range for list_of_queues")


def check_arrival(arrival: int):
    if arrival >= STOP:
        return INFINITY
    else:
        return arrival


class Track:
    def __init__(self, num_serv, num_queue):
        self.node = 0.0  # time integrated number in the node
        self.queue = 0.0  # time integrated number in the queue
        self.service = [0.0] * num_serv  # time integrated number in service
        self.service_color = [0.0] * num_queue
        self.service_preemptive = 0.0
        self.jobs_completed = [0] * num_serv
        self.jobs_complete_color = [0] * num_queue
        self.wait_time = [0.0] * num_queue
        self.delay_time = [0.0] * num_queue


class Time:
    def __init__(self, num_serv):
        self.arrival = -1  # next arrival time
        self.completion = [INFINITY] * num_serv  # next completion times for each server
        self.min_completion = INFINITY
        self.server_index = -1
        self.current = -1  # current time
        self.next = -1  # next (most imminent) event time
        self.last = -1  # last arrival time


def next_event(current_triage: int, current_queue: int, t_analisi: list):
    prox_evento = INFINITY
    for i in range(len(t_analisi)):
        if t_analisi[i].current > 0:
            prox_evento = min(prox_evento, t_analisi[i].current)
            #print("Analisi num", i, t_analisi[i].current, "Min: ", prox_evento)

    if current_queue > 0:
        prox_evento = min(prox_evento, current_queue)
        #print("Queue", current_queue, "Min: ", prox_evento)

    if current_triage > 0:
        prox_evento = min(prox_evento, current_triage)
        #print("Triage", current_triage, "Min: ", prox_evento)

    if prox_evento >= INFINITY:
        prox_evento = -1

    #print("Evento minimo", prox_evento)

    return prox_evento


def next_eventt(t_triage: Time, t_queue: Time, t_analisi: list):
    prox_evento = INFINITY
    for i in range(len(t_analisi)):
        if t_analisi[i].current > 0:
            prox_evento = min(prox_evento, t_analisi[i].current)
    if t_queue.min_completion > 0:
        prox_evento = min(prox_evento, t_queue.min_completion)
    if t_queue.min_completion > 0:
        prox_evento = min(prox_evento, t_queue.min_completion)
    print(prox_evento)

    return prox_evento
