from utility.Rngs import random, selectStream
from utility.Utils import *
from utility.Parameters import *

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


def pre_process_triage():
    return 0


