from controller.TriageController import *
from controller.QueueController import *
from controller.ExamsQueueController import *
from controller.EsamiController import *

arrivalTemp = START  # global temp var for getArrival function
analisi_1_volta = 0
analisi_2_volte = 0
analisi_3_volte = 0
analisi_piu_3 = 0
plantSeeds(DEFAULT)


def simulation():
    global number_Analisi, index_Analisi, queue_Analis, analisi_1_volta, analisi_2_volte, analisi_piu_3, analisi_3_volte
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
        prox_operazione = next_event(t_triage.current, t_queue.current, t_Analisi)
        #print ("tempi queue: ", t_queue.completion)
        switch(prox_operazione, t_triage, t_queue, t_Analisi)

        #print("num: ", number_triage, number_queue, number_Analisi[0], number_Analisi[1], number_Analisi[2], number_Analisi[3], number_Analisi[4], number_Analisi[5])
        #print("")
        #print("")
        #print("")
    triage_data(area_triage, t_triage, queue_triage)
    queue_data(area_queue, t_queue, queue)
    analisi_data(area_Analisi, t_Analisi, queue_Analisi)

    print("Analisi: ", sum(index_Analisi))
    print("Queue  : ", index_queue)
    print("Triage : ", index_triage)
    print("Job che hanno fatto esami 1 volta: ", analisi_1_volta)
    print("Job che hanno fatto esami 2 volte: ", analisi_2_volte)
    print("Job che hanno fatto esami 3 volte: ", analisi_3_volte)
    print("Job che hanno fatto esami 4 volte: ", analisi_piu_3)


def processa_arrivo_triage():
    global number_triage, arrivalTemp
    number_triage += 1
    job = Job(arrivalTemp)
    job.triage(give_code())
    arrivalTemp = arrivalTemp + GetArrival()
    add_job_to_queue(job, queue_triage)
    t_triage.arrival = arrivalTemp
    arrival_triage(t_triage, servers_busy_triage, queue_triage)


def processa_completamento_triage():
    global index_triage, number_triage, number_queue
    index_triage += 1
    number_triage -= 1

    job_completed = completion_triage(t_triage, servers_busy_triage, queue_triage, area_triage)
    job_completed.set_time_triage(t_triage.current - job_completed.get_arrival_temp())
    # print("Pre:", job_completed.get_arrival_temp())
    job_completed.set_arrival_temp(t_triage.current)
    # print("Post:", job_completed.get_arrival_temp())
    number_queue += 1
    pass_to_queue(job_completed, queue)
    t_queue.arrival = check_arrival(t_triage.arrival + STOP)  # DA RIVEDERE
    # print("T_Queue_a:", t_queue.arrival)


def processa_completamento_queue():
    global index_queue, number_queue, analisi_3_volte, analisi_2_volte, analisi_piu_3, analisi_1_volta

    index_queue += 1
    number_queue -= 1
    job_to_analisi = completion_queue(t_queue, servers_busy_queue, queue, area_queue)

    job_to_analisi.set_queue_time(
        t_queue.min_completion - (job_to_analisi.get_arrival_temp() + job_to_analisi.get_time_triage()))

    if probabilita_analisi(job_to_analisi.get_uscita()):
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
        job_to_analisi.set_arrival_temp(t_queue.current)
        number_Analisi[analisi] += 1
    #print("UNA VOLTA: ", analisi_1_volta, "2 VOLTE: ", analisi_2_volte, "3 VOLTE: ", analisi_3_volte, "4 VOLTE: ",analisi_piu_3)


def processa_completamento_analisi(index_analisi):
    global number_triage, number_queue
    index_Analisi[index_analisi] += 1
    number_Analisi[index_analisi] -= 1
    job_to_out = completion_analisi(t_Analisi[index_analisi], servers_busy_Analisi[index_analisi],
                                    queue_Analisi[index_analisi],
                                    area_Analisi[index_analisi], index_analisi)

    lista_analisi = job_to_out.get_lista_analisi()

    if len(lista_analisi) > 1:
        #print("LISTA ANALISI: ", lista_analisi)
        # print("index", index_analisi, "job infame", job_to_out.get_id())
        # print("l.a: ", lista_analisi)
        # print("a.d: ", analisi_disponibili[index_analisi])

        lista_analisi.remove(analisi_disponibili[index_analisi])

        # print(job_to_out.get_id(), lista_analisi)
        job_to_out.set_lista_analisi(lista_analisi)
        analisi = pass_to_analisi(job_to_out, queue_Analisi, t_queue)
        job_to_out.set_arrival_temp(t_Analisi[analisi].current)
        number_Analisi[analisi] += 1
        # print(" ID: ", job_to_out.get_id(), "VALORE USCITA:", job_to_out.get_uscita())

    else:
        #print("SONO QUI")
        number_queue += 1
        # print("PRE AGGIORNAMENTO ID: ", job_to_out.get_id(), "VALORE USCITA:", job_to_out.get_uscita())
        job_to_out.set_uscita()
        # print("POST AGGIORNAMENTO",job_to_out.get_id(), "VALORE USCITA: ", job_to_out.get_uscita())
        return_to_queue(job_to_out, queue, t_triage)
        t_queue.arrival = check_arrival(t_triage.arrival)  # DA RIVEDERE
        job_to_out.set_arrival_temp(t_queue.current)


def main():
    simulation()


def switch(prox_operazione, t_triage: Time, t_queue: Time, t_analisi: list):
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


if __name__ == "__main__":
    main()
