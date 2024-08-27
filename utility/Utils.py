from utility import Parameters
from utility.Parameters import INFINITY, TEMPO_LIMITE, START, OBIETTIVO_MIGLIORATIVO
import subprocess
import shlex


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
        self.service_preemption = [0.0] * num_queue

        self.num_queue = num_queue
        self.num_serv = num_serv

    def reset(self):
        self.node = 0.0  # time integrated number in the node
        self.queue = 0.0  # time integrated number in the queue
        self.service = [0.0] * self.num_serv  # time integrated number in service
        self.service_color = [0.0] * self.num_queue
        self.service_preemptive = 0.0
        self.service_preemption = [0.0] * self.num_queue
        self.jobs_completed = [0] * self.num_serv
        self.jobs_complete_color = [0] * self.num_queue
        self.wait_time = [0.0] * self.num_queue
        self.delay_time = [0.0] * self.num_queue


class Time:
    def __init__(self, num_serv):
        self.arrival = -1  # next arrival time
        self.completion = [INFINITY] * num_serv  # next completion times for each server
        self.min_completion = INFINITY
        self.server_index = -1
        self.current = -1  # current time
        self.next = -1  # next (most imminent) event time
        self.last = -1  # last arrival time
        self.num_serv = num_serv

    def reset(self):
        self.arrival = -1
        self.completion = [INFINITY] * self.num_serv
        self.min_completion = INFINITY
        self.server_index = -1
        self.current = -1
        self.next = -1
        self.last = -1

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


def get_job_old(list_of_queues, t):
    """Selects the next job to serve based on a priority policy"""
    if Parameters.migliorativo:
        for queue in list_of_queues:
            if queue and queue[0] and (t.current - queue[0].get_id()) > OBIETTIVO_MIGLIORATIVO[
                queue[0].get_codice() - 1]:
                return queue.pop(0)
    else:
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
    if arrival >= Parameters.STOP:
        return INFINITY
    else:
        return arrival


def next_event(current_triage: int, current_queue: int, t_analisi: list):
    prox_evento = INFINITY
    for i in range(len(t_analisi)):
        if t_analisi[i].current > 0:
            prox_evento = min(prox_evento, t_analisi[i].current)

    if current_queue > 0:
        prox_evento = min(prox_evento, current_queue)

    if current_triage > 0:
        prox_evento = min(prox_evento, current_triage)

    if prox_evento >= INFINITY:
        prox_evento = -1

    return prox_evento


def initialize_arrival(t):
    t.arrival = START
    t.current = START


def get_next_job_to_serve(list_of_queues, t: Time = 0):
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


def max_value(t_analisi: list, t_last1: float, t_last2: float):
    maximum = max(t_last1, t_last2)
    for i in range(len(t_analisi)):
        if t_analisi[i].last > maximum:
            maximum = t_analisi[i].last
    return maximum


def generate_path_plot(modality, better, white):
    if modality.lower() == "finite":
        modality_value = "finite//"
    elif modality.lower() == "infinite":
        modality_value = "infinite//"
    else:
        raise ValueError("Il valore di modality deve essere 'finite' o 'infinite'.")
    improvement = "migliorativo//" if "true" == better else "standard//"
    white_status = "bianchi_dimezzati" if "true" == white else "bianchi_standard"
    result_string = modality_value + improvement + white_status
    return result_string


def execute_parallel_simulations():
    commands = [
        "python3 main.py -m finite -b true ",  # Finita, migliorativa, bianchi normali
        "python3 main.py -m finite",  # Finita, standard, bianchi normali
        "python3 main.py -m finite -b true -w true",  # Finita, migliorativa, bianchi dimezzati
        "python3 main.py -m finite -w true",  # Finita, standard, bianchi dimezzati
        "python3 main.py -m infinite -b true",  # Infinita, migliorativa, bianchi normali
        "python3 main.py -m infinite",  # Infinita, standard, bianchi normali
        "python3 main.py -m infinite -b true -w true",  # Infinita, migliorativa, bianchi dimezzati
        "python3 main.py -m infinite -w true"  # Infinita, standard, bianchi dimezzati
    ]
    # Comando per avviare una nuova finestra del terminale
    terminal_cmd_template = "start cmd /k {cmd}"

    processes = []
    for cmd in commands:
        # Format the command to start a new terminal window with the simulation command
        terminal_cmd = terminal_cmd_template.format(cmd=cmd)
        processes.append(subprocess.Popen(terminal_cmd, shell=True))

    # Attendi che tutti i processi siano terminati
    for p in processes:
        p.wait()
