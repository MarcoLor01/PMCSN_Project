from controller.TriageController import *
from controller.QueueController import *
from controller.ExamsQueueController import *
from controller.EsamiController import *

summary = 0
max_simulation = 2000000
step_size = 500
iteration = 0
arrivalTemp = START  # global temp var for getArrival function

plantSeeds(DEFAULT)


def simulation():
    # Importiamo singolarmente o un vettore?
    # global number_Ecg, index_Ecg, queue_Ecg
    # global number_Emocromo, index_Emocromo, queue_Emocromo
    # global number_Tac, index_Tac, queue_Tac
    # global number_Radiografia, index_Radiografia, queue_Radiografia
    # global number_altriEsami, index_altriEsami, queue_altriEsami
    global number_Analisi, index_Analisi, queue_Analis
    global arrivalTemp
    global number_triage, index_triage, queue_triage
    global number_queue, index_queue, queue

    arrivalTemp = START
    arrivalTemp = arrivalTemp + GetArrival()
    init_triage(arrivalTemp)
    init_queue()
    init_analisi(t_Analisi, area_Analisi, queue_Analisi)

    while (t_triage.arrival < STOP) or (number_triage > 0) or (number_queue > 0) or (max(number_Analisi) > 0):
        pre_process_triage(t_triage, area_triage, number_triage, servers_busy_triage)
        pre_process_queue(area_queue, number_queue, servers_busy_queue)
        pre_process_analisi(t_Analisi, area_Analisi, number_Analisi, servers_busy_Analisi)
        #print(t_triage.current, t_Analisi[0].current, t_queue.current)
        if t_triage.current == t_triage.arrival and t_triage.current < INFINITY:  # process an arrival
            number_triage += 1
            #print("A:", arrivalTemp)
            job = Job(arrivalTemp)
            job.triage(give_code())
            arrivalTemp = arrivalTemp + GetArrival()
            add_job_to_queue(job, queue_triage)
            t_triage.arrival = arrivalTemp
            arrival_triage(t_triage, servers_busy_triage, queue_triage)

        elif t_triage.current == t_triage.min_completion and t_triage.current < INFINITY:  # process a completion for triage
            index_triage += 1
            number_triage -= 1
            job_completed = completion_triage(t_triage, servers_busy_triage, queue_triage, area_triage)
            job_completed.set_time_triage(t_triage.min_completion - job_completed.get_arrival_temp())
            job_completed.set_arrival_temp(t_queue.current)
            number_queue += 1
            pass_to_queue(job_completed, queue, t_triage)
            t_queue.arrival = check_arrival(t_triage.arrival)  # DA RIVEDERE

        if t_queue.current == t_queue.min_completion and number_queue > 0:  # process a completion
            index_queue += 1
            number_queue -= 1
            job_to_analisi = completion_queue(t_queue, servers_busy_queue, queue, area_queue)
            job_to_analisi.set_queue_time(
                t_queue.min_completion - (job_to_analisi.get_arrival_temp() + job_to_analisi.get_time_triage()))
            lista_analisi = get_analisi()
            job_to_analisi.set_lista_analisi(lista_analisi)
            analisi = pass_to_analisi(job_to_analisi, queue_Analisi, t_queue)
            job_to_analisi.set_arrival_temp(t_Analisi[analisi].current)
            number_Analisi[analisi] += 1

        for i in range(len(t_Analisi)):
            if t_Analisi[i].current == t_Analisi[i].min_completion and number_Analisi[i] > 0:  # process a completion
                index_Analisi[i] += 1
                number_Analisi[i] -= 1
                job_to_out = completion_analisi(t_Analisi[i], servers_busy_Analisi[i], queue_Analisi[i],
                                                area_Analisi[i], i)

    triage_data(area_triage, t_triage, queue_triage)
    queue_data(area_queue, t_queue, queue)
    analisi_data(area_Analisi, t_Analisi, queue_Analisi)

    print("Analisi: ", sum(index_Analisi))
    print("Queue  : ", index_queue)
    print("Triage : ", index_triage)


def main():
    simulation()


if __name__ == "__main__":
    main()
