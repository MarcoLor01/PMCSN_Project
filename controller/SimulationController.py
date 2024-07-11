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
        switch(prox_operazione, t_triage, t_queue, t_Analisi)
        #prox_operazione = next_eventt(t_triage, t_queue, t_Analisi)

        #print("num: ", number_triage, number_queue, min(number_Analisi), max(number_Analisi))

        #        if t_triage.current == t_triage.arrival and t_triage.current < INFINITY:  # process an arrival
        #            number_triage += 1
        #            job = Job(arrivalTemp)
        #            job.triage(give_code())
        #            arrivalTemp = arrivalTemp + GetArrival()
        #            add_job_to_queue(job, queue_triage)
        #            t_triage.arrival = arrivalTemp
        #            arrival_triage(t_triage, servers_busy_triage, queue_triage)
        #
        #        elif t_triage.current == t_triage.min_completion and t_triage.current < INFINITY:
        #            # process a completion for triage
        #            index_triage += 1
        #            number_triage -= 1
        #            job_completed = completion_triage(t_triage, servers_busy_triage, queue_triage, area_triage)
        #            job_completed.set_time_triage(t_triage.min_completion - job_completed.get_arrival_temp())
        #            #print("Pre:", job_completed.get_arrival_temp())
        #            job_completed.set_arrival_temp(t_queue.current)
        #            #print("Post:", job_completed.get_arrival_temp())
        #            number_queue += 1
        #            pass_to_queue(job_completed, queue, t_triage)
        #            t_queue.arrival = check_arrival(t_triage.arrival)  # DA RIVEDERE
        #            #print("T_Queue_a:", t_queue.arrival)

        #        if t_queue.current == t_queue.min_completion and number_queue > 0:
        #            # process a completion
        #            index_queue += 1
        #            number_queue -= 1
        #            job_to_analisi = completion_queue(t_queue, servers_busy_queue, queue, area_queue)
        #
        #            job_to_analisi.set_queue_time(
        #                t_queue.min_completion - (job_to_analisi.get_arrival_temp() + job_to_analisi.get_time_triage()))
        #
        #            if probabilita_analisi(job_to_analisi.get_uscita()):
        #                if job_to_analisi.get_uscita() == 0:
        #                    analisi_1_volta += 1
        #                    #print("ARRIVAL TEMP ANALISI: ", job_to_analisi.get_arrival_temp(), "VALORE GET USCITA: ",job_to_analisi.get_id())
        #
        #                elif job_to_analisi.get_uscita() == 1:
        #                    analisi_2_volte += 1
        #                elif job_to_analisi.get_uscita() == 2:
        #                    analisi_3_volte += 1
        #                if job_to_analisi.get_uscita() > 2:
        #                    analisi_piu_3 += 1
        #
        #                lista_analisi = get_analisi()
        #                job_to_analisi.set_lista_analisi(lista_analisi)
        #                analisi = pass_to_analisi(job_to_analisi, queue_Analisi, t_queue)
        #                job_to_analisi.set_arrival_temp(t_Analisi[analisi].current)
        #                number_Analisi[analisi] += 1
        #
        #        for i in range(len(t_Analisi)):
        #
        #            if t_Analisi[i].current == t_Analisi[i].min_completion and number_Analisi[i] > 0:  # process a completion
        #                index_Analisi[i] += 1
        #                number_Analisi[i] -= 1
        #                job_to_out = completion_analisi(t_Analisi[i], servers_busy_Analisi[i], queue_Analisi[i],
        #                                                area_Analisi[i], i)
        #
        #                lista_analisi = job_to_out.get_lista_analisi()
        #
        #                if len(lista_analisi) > 1:
        #                    #print("index", i, "                  job infame", job_to_out.get_id())
        #                    #print("l.a: ", lista_analisi)
        #                    #print("a.d: ", analisi_disponibili[i])
        #
        #                    lista_analisi.remove(analisi_disponibili[i])
        #
        #                    #print(job_to_out.get_id(), lista_analisi)
        #                    job_to_out.set_lista_analisi(lista_analisi)
        #                    analisi = pass_to_analisi(job_to_out, queue_Analisi, t_queue)
        #                    job_to_out.set_arrival_temp(t_Analisi[analisi].current)
        #                    number_Analisi[analisi] += 1
        #                    #print(" ID: ", job_to_out.get_id(), "VALORE USCITA:", job_to_out.get_uscita())
        #
        #                else:
        #                    number_queue += 1
        #                    #print("PRE AGGIORNAMENTO ID: ", job_to_out.get_id(), "VALORE USCITA:", job_to_out.get_uscita())
        #                    job_to_out.set_uscita()
        #                    #print("POST AGGIORNAMENTO",job_to_out.get_id(), "VALORE USCITA: ", job_to_out.get_uscita())
        #                    return_to_queue(job_to_out, queue, t_triage)
        #                    t_queue.arrival = check_arrival(t_triage.arrival)  # DA RIVEDERE
        #                    job_to_out.set_arrival_temp(t_queue.current)
        #
        print("num: ", number_triage, number_queue, min(number_Analisi), sum(number_Analisi))

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


def switch(prox_operazione, t_triage: Time, t_queue: Time, t_analisi: list):
    print (prox_operazione)
    #if prox_operazione > INFINITY:
    #    return
    if prox_operazione == t_triage.arrival:
        processa_arrivo_triage()
        print("triage 1                      fatto")
    elif prox_operazione == t_triage.min_completion:
        processa_completamento_triage()
        print("triage 2                       fatto")
    elif prox_operazione == t_queue.min_completion:
        processa_completamento_queue()
        print("queue                       fatto")
    else:
        print("tq", t_queue.min_completion)
        for i in range(len(t_analisi)):
            print("CURRENT ANALISI: ", t_analisi[i].current, "MIN COMPL: ", t_Analisi[i].min_completion, "COMPLETION: ", t_Analisi[i].completion)
            if t_analisi[i].current == t_analisi[i].min_completion:
                processa_completamento_analisi(i)
                break


def processa_arrivo_triage():
    global number_triage, arrivalTemp
    print("PRE TRIAGE ARRIVAL:", t_triage.arrival)

    number_triage += 1
    job = Job(arrivalTemp)
    job.triage(give_code())
    arrivalTemp = arrivalTemp + GetArrival()
    add_job_to_queue(job, queue_triage)
    t_triage.arrival = arrivalTemp
    arrival_triage(t_triage, servers_busy_triage, queue_triage)
    print("POST TRIAGE ARRIVAL:", t_triage.arrival)


def processa_completamento_triage():
    global index_triage, number_triage, number_queue
    index_triage += 1
    number_triage -= 1
    print("PRE TRIAGE:", t_triage.completion)

    job_completed = completion_triage(t_triage, servers_busy_triage, queue_triage, area_triage)
    job_completed.set_time_triage(t_triage.min_completion - job_completed.get_arrival_temp())
    # print("Pre:", job_completed.get_arrival_temp())
    job_completed.set_arrival_temp(t_queue.current)
    # print("Post:", job_completed.get_arrival_temp())
    number_queue += 1
    pass_to_queue(job_completed, queue, t_triage)
    t_queue.arrival = check_arrival(t_triage.arrival + STOP)  # DA RIVEDERE
    # print("T_Queue_a:", t_queue.arrival)
    print("POST TRIAGE:", t_triage.completion)


def processa_completamento_queue():
    global index_queue, number_queue, analisi_3_volte, analisi_2_volte, analisi_piu_3, analisi_1_volta
    print("PRE QUEUE:", t_queue.completion)

    index_queue += 1
    number_queue -= 1
    job_to_analisi = completion_queue(t_queue, servers_busy_queue, queue, area_queue)

    job_to_analisi.set_queue_time(
        t_queue.min_completion - (job_to_analisi.get_arrival_temp() + job_to_analisi.get_time_triage()))

    if probabilita_analisi(job_to_analisi.get_uscita()):
        if job_to_analisi.get_uscita() == 0:
            analisi_1_volta += 1
            # print("ARRIVAL TEMP ANALISI: ", job_to_analisi.get_arrival_temp(), "VALORE GET USCITA: ",job_to_analisi.get_id())

        elif job_to_analisi.get_uscita() == 1:
            analisi_2_volte += 1
        elif job_to_analisi.get_uscita() == 2:
            analisi_3_volte += 1
        if job_to_analisi.get_uscita() > 2:
            analisi_piu_3 += 1

        lista_analisi = get_analisi()
        job_to_analisi.set_lista_analisi(lista_analisi)
        analisi = pass_to_analisi(job_to_analisi, queue_Analisi, t_queue)
        job_to_analisi.set_arrival_temp(t_Analisi[analisi].current)
        number_Analisi[analisi] += 1
        print("POST QUEUE:", t_queue.completion)


def processa_completamento_analisi(index_analisi):
    global number_triage, number_queue
#if number_Analisi[index_analisi] > 0:  # process a completion
    index_Analisi[index_analisi] += 1
    number_Analisi[index_analisi] -= 1
    print("t_analisi                           ", i, t_Analisi[index_analisi])
    job_to_out = completion_analisi(t_Analisi[index_analisi], servers_busy_Analisi[index_analisi],
                                    queue_Analisi[index_analisi],
                                    area_Analisi[index_analisi], index_analisi)

    lista_analisi = job_to_out.get_lista_analisi()

    if len(lista_analisi) > 1:
        # print("index", index_analisi, "job infame", job_to_out.get_id())
        # print("l.a: ", lista_analisi)
        # print("a.d: ", analisi_disponibili[index_analisi])

        #lista_analisi.remove(analisi_disponibili[index_analisi])
        lista_analisi.pop(0)

        # print(job_to_out.get_id(), lista_analisi)
        job_to_out.set_lista_analisi(lista_analisi)
        analisi = pass_to_analisi(job_to_out, queue_Analisi, t_queue)
        job_to_out.set_arrival_temp(t_Analisi[analisi].current)
        number_Analisi[analisi] += 1
        # print(" ID: ", job_to_out.get_id(), "VALORE USCITA:", job_to_out.get_uscita())

    else:
        number_queue += 1
        # print("PRE AGGIORNAMENTO ID: ", job_to_out.get_id(), "VALORE USCITA:", job_to_out.get_uscita())
        job_to_out.set_uscita()
        # print("POST AGGIORNAMENTO",job_to_out.get_id(), "VALORE USCITA: ", job_to_out.get_uscita())
        return_to_queue(job_to_out, queue, t_triage)
        t_queue.arrival = check_arrival(t_triage.arrival)  # DA RIVEDERE
        job_to_out.set_arrival_temp(t_queue.current)

    print("num: ", number_triage, number_queue, min(number_Analisi), sum(number_Analisi))


def main():
    simulation()


if __name__ == "__main__":
    main()
