from controller.TriageController import *
from controller.QueueController import *
from controller.ExamsQueueController import *
from controller.EsamiController import *
from utility.Rngs import plantSeeds, DEFAULT
from utility.SimulationUtils import stat, stats

arrivalTemp = START  # global temp var for getArrival function
plantSeeds(DEFAULT)


def simulation(stop = STOP):

    global number_Analisi, index_Analisi, queue_Analis, analisi_1_volta, analisi_2_volte, analisi_piu_3, analisi_3_volte
    global arrivalTemp
    global number_triage, index_triage, queue_triage
    global number_queue, index_queue, queue
    analisi_1_volta = 0
    analisi_2_volte = 0
    analisi_3_volte = 0
    analisi_piu_3 = 0
    arrivalTemp = START
    arrivalTemp = arrivalTemp + GetArrival()
    init_triage(arrivalTemp)
    init_queue()
    init_analisi(t_Analisi, area_Analisi, queue_Analisi)

    while t_triage.arrival < stop or number_triage > 0 or number_queue > 0 or max(number_Analisi) > 0:
        pre_process_triage(t_triage, area_triage, number_triage, servers_busy_triage)
        pre_process_queue(area_queue, number_queue, servers_busy_queue)
        pre_process_analisi(t_Analisi, area_Analisi, number_Analisi, servers_busy_Analisi)
        prox_operazione = next_event(t_triage.current, t_queue.current, t_Analisi)
        switch(prox_operazione, t_triage, t_queue, t_Analisi)
    t_triage.last = t_queue.last = t_Analisi[0].last = t_Analisi[1].last = t_Analisi[2].last = t_Analisi[3].last = t_Analisi[4].last = t_Analisi[5].last = max_value(t_Analisi, t_triage.last, t_queue.last)
#     if prox_operazione < INFINITY:
#         t_triage.last = prox_operazione
#         t_queue.last = prox_operazione
#         for i in range(len(t_analisi)):
#             t_analisi[i].last = prox_operazione

    triage_data_rec(area_Analisi[0], t_Analisi[0], queue_Analisi[0])
    #queue_data(area_queue, t_queue, queue)
    #analisi_data(area_Analisi, t_Analisi, queue_Analisi)
#    print("Analisi: ", sum(index_Analisi))
#    print("Queue  : ", index_queue)
#    print("Triage : ", index_triage)
#    print("Job che hanno fatto esami 1 volta: ", analisi_1_volta)
#    print("Job che hanno fatto esami 2 volte: ", analisi_2_volte)
#    print("Job che hanno fatto esami 3 volte: ", analisi_3_volte)
#    print("Job che hanno fatto esami 4 volte: ", analisi_piu_3)
    return stat(t_triage, area_triage), stat(t_queue, area_queue), stats(t_Analisi, area_Analisi)


def processa_arrivo_triage():
    global number_triage, arrivalTemp
    number_triage += 1
    job = Job(arrivalTemp)
    job.triage(give_code())
    arrivalTemp += GetArrival()
    add_job_to_queue(job, queue_triage)
    t_triage.arrival = arrivalTemp
    arrival_triage(t_triage, servers_busy_triage, queue_triage)


def processa_completamento_triage():
    global index_triage, number_triage, number_queue
    index_triage += 1
    number_triage -= 1

    job_completed = completion_triage(t_triage, servers_busy_triage, queue_triage, area_triage)
    job_completed.set_tempo_rimanente(0)

    if job_completed.get_codice() == 1 or job_completed.get_codice() == 2 or scegli_azione():
        number_queue += 1
        pass_to_queue(job_completed, queue)
        t_queue.arrival = check_arrival(t_triage.arrival + STOP)


def processa_completamento_queue():
    global index_queue, number_queue, analisi_3_volte, analisi_2_volte, analisi_piu_3, analisi_1_volta

    index_queue += 1
    number_queue -= 1
    job_to_analisi = completion_queue(t_queue, servers_busy_queue, queue, area_queue)

    if probability_analisi(job_to_analisi.get_uscita()):
        if job_to_analisi.get_uscita() == 0:
            analisi_1_volta += 1
        elif job_to_analisi.get_uscita() == 1:
            analisi_2_volte += 1
        elif job_to_analisi.get_uscita() == 2:
            analisi_3_volte += 1
        if job_to_analisi.get_uscita() > 2:
            analisi_piu_3 += 1

        lista_analisi = get_analisi()
        job_to_analisi.set_lista_analisi(lista_analisi)
        analisi = pass_to_analisi(job_to_analisi, queue_Analisi, t_queue)
        number_Analisi[analisi] += 1


def processa_completamento_analisi(index_analisi):
    global number_triage, number_queue
    index_Analisi[index_analisi] += 1
    number_Analisi[index_analisi] -= 1
    job_to_out = completion_analisi(t_Analisi[index_analisi], servers_busy_Analisi[index_analisi],
                                    queue_Analisi[index_analisi],
                                    area_Analisi[index_analisi], index_analisi)

    lista_analisi = job_to_out.get_lista_analisi()

    if len(lista_analisi) > 1:
        lista_analisi.remove(analisi_disponibili[index_analisi])
        job_to_out.set_lista_analisi(lista_analisi)
        analisi = pass_to_analisi(job_to_out, queue_Analisi, t_queue)
        job_to_out.set_arrival_temp(t_Analisi[analisi].current)
        number_Analisi[analisi] += 1
    else:
        number_queue += 1
        job_to_out.set_uscita()
        job_to_out.set_tempo_rimanente(0)
        job_to_out.set_arrival_temp(t_Analisi[0].current)
        return_to_queue(job_to_out, queue, t_triage)
        t_queue.arrival = check_arrival(t_triage.arrival)


def switch(prox_operazione, t_triage, t_queue, t_analisi):
    t_triage.current = prox_operazione
    t_queue.current = prox_operazione
    for i in range(len(t_analisi)):
        t_analisi[i].current = prox_operazione

    if prox_operazione == t_triage.arrival:
        processa_arrivo_triage()
    elif prox_operazione == t_triage.min_completion:
        processa_completamento_triage()
    elif prox_operazione == t_queue.min_completion:
        processa_completamento_queue()
    else:
        for i in range(len(t_analisi)):
            if prox_operazione == t_analisi[i].min_completion:
                processa_completamento_analisi(i)
                break


def reset():
    global index_triage, index_queue, index_Analisi
    t_triage.reset()
    area_triage.reset()
    index_triage = 0

    t_queue.reset()
    area_queue.reset()
    index_queue = 0

    for i in range(len(t_Analisi)):
        t_Analisi[i].reset()
        area_Analisi[i].reset()
        index_Analisi[i] = 0


if __name__ == "__main__":
    #for i in range (5):
    print("Simulazione n ", i)
    print (simulation())
    reset()
