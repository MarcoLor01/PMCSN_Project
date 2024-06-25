from model.Job import Job
from utility.CodeEnum import Code
from utility.Rngs import random, selectStream


def giveCode(job: Job):
    selectStream(1)
    code = assign_triage_code()
    job.triage(code)
    return job


def assign_triage_code():
    # Lista dei codici corrispondenti
    codes = [Code.ROSSO, Code.ARANCIONE, Code.BLU, Code.VERDE, Code.BIANCO]
    # Probabilità cumulative corrispondenti
    cumulative_probabilities = [0.063, 0.259, 0.642, 0.948, 1.0]  # Probabilità cumulative

    rand_num = random()

    # Determinare il codice basato sul numero casuale
    for code, cum_prob in zip(codes, cumulative_probabilities):
        if rand_num < cum_prob:
            return code
