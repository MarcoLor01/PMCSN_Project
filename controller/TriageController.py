from model.Job import Job
from utility.CodeEnum import Code
from utility.Rngs import random, selectStream


def giveCode():
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
