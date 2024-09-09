from controller.TriageController import *
from controller.QueueController import *
from controller.ExamsQueueController import *
from controller.EsamiController import *
from utility.SimulationUtils import stat, stats, stat_batch, stats_batch

arrivalTemp = START  # global temp var for getArrival function

departed_job = 0
violations = [0] * 5
violation = [[], [], [], [], []]


#plantSeeds(DEFAULT)


def simulation(stop, batch_size = 1, number_valid_batch = 64):
    global number_Analisi, index_Analisi, queue_Analis, analisi_1_volta, analisi_2_volte, analisi_piu_3, analisi_3_volte, departed_job
    global arrivalTemp
    global number_triage, index_triage, queue_triage
    global number_queue, index_queue, queue

    printed_status = {
        "25%": False,
        "50%": False,
        "75%": False,
        "100%": False
    }
    reset()
    analisi_1_volta = 0
    analisi_2_volte = 0
    analisi_3_volte = 0
    analisi_piu_3 = 0
    NUMERO_CODICI = 5
    NUMERO_CODE_Q = 7
    NUMERO_CODE_A = 2
    current_batch = 0
    batch_number = 0
    graph_data = [[],[],[],[],[],[],[]]
    campionamento = 100
    valore_campionamento_corrente = 0

    jobs_complete_batch_triage = [0.0] * NUMERO_CODICI
    delay_times_batch_triage = [0.0] * NUMERO_CODICI
    service_batch_triage = [0.0] * NUMERO_DI_SERVER_TRIAGE
    wait_time_batch_triage = [0.0] * NUMERO_CODICI

    jobs_complete_batch_queue = [0.0] * NUMERO_CODE_Q
    delay_times_batch_queue = [0.0] * NUMERO_CODE_Q
    service_batch_queue = [0.0] * NUMERO_DI_SERVER_QUEUE
    wait_time_batch_queue = [0.0] * NUMERO_CODE_Q

    jobs_complete_batch_analisi = [[0.0] * NUMERO_CODE_A] * NUMERO_DI_ANALISI
    delay_times_batch_analisi = [[0.0] * NUMERO_CODE_A] * NUMERO_DI_ANALISI
    service_batch_analisi = [0.0] * NUMERO_DI_ANALISI
    for analisi in range(NUMERO_DI_ANALISI):
        service_batch_analisi[analisi] = [0.0] * NUMERO_SERVER_ANALISI[analisi]

    wait_time_batch_analisi = [[0.0] * NUMERO_CODE_A] * NUMERO_DI_ANALISI

    utilization_batch_triage = []
    response_batch_triage = []
    delay_batch_triage = []
    utilization_batch_queue = []
    response_batch_queue = []
    delay_batch_queue = []
    utilization_batch_analisi = []
    response_batch_analisi = []
    delay_batch_analisi = []
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
        monitor_simulation(prox_operazione, stop, printed_status)
        switch(prox_operazione, t_triage, t_queue, t_Analisi)

        if prox_operazione-valore_campionamento_corrente > campionamento:
            for i in range(len(queue)):
                graph_data[i].append(len(queue[i]))
            valore_campionamento_corrente = prox_operazione
        if (batch_size > 1 and departed_job % batch_size == 0 and departed_job != 0) or (
                batch_size == 1 and departed_job % 100 == 0 and departed_job != 0):

            res_t = stat_batch(t_triage, area_triage, service_batch_triage, current_batch,
                               jobs_complete_batch_triage, wait_time_batch_triage, delay_times_batch_triage)
            res_q = stat_batch(t_queue, area_queue, service_batch_queue, current_batch, jobs_complete_batch_queue,
                               wait_time_batch_queue, delay_times_batch_queue)
            res_a = stats_batch(t_Analisi, area_Analisi, service_batch_analisi, current_batch,
                                jobs_complete_batch_analisi, wait_time_batch_analisi, delay_times_batch_analisi)

            add = True

            if len(res_t[1]) != 5 or len(res_t[2]) != 5 or len(res_q[1]) != 7 or len(res_q[2]) != 7:
                add = False

            for i in range(0, NUMERO_DI_ANALISI):
                if len(res_a[1][i]) != 2 or len(res_a[2][i]) != 2:
                    add = False

            if add and batch_number < number_valid_batch:
                utilization_batch_triage += res_t[0]
                response_batch_triage += res_t[1]
                delay_batch_triage += res_t[2]
                utilization_batch_queue += res_q[0]
                response_batch_queue += res_q[1]
                delay_batch_queue += res_q[2]
                utilization_batch_analisi += res_a[0]
                response_batch_analisi += res_a[1]
                delay_batch_analisi += res_a[2]
                batch_number += 1

            current_batch = t_queue.current

            jobs_complete_batch_triage = area_triage.jobs_complete_color.copy()
            wait_time_batch_triage = area_triage.wait_time.copy()
            service_batch_triage = area_triage.service.copy()
            delay_times_batch_triage = area_triage.delay_time.copy()

            jobs_complete_batch_queue = area_queue.jobs_complete_color.copy()
            wait_time_batch_queue = area_queue.wait_time.copy()
            service_batch_queue = area_queue.service.copy()
            delay_times_batch_queue = area_queue.delay_time.copy()

            for i in range(len(area_Analisi)):
                jobs_complete_batch_analisi[i] = area_Analisi[i].jobs_complete_color.copy()
                wait_time_batch_analisi[i] = area_Analisi[i].wait_time.copy()
                service_batch_analisi[i] = area_Analisi[i].service.copy()
                delay_times_batch_analisi[i] = area_Analisi[i].delay_time.copy()

            departed_job = 0
    batch_res = [[utilization_batch_triage, response_batch_triage, delay_batch_triage],
                 [utilization_batch_queue, response_batch_queue, delay_batch_queue],
                 [utilization_batch_analisi, response_batch_analisi, delay_batch_analisi]]
    t_triage.last = t_queue.last = t_Analisi[0].last = t_Analisi[1].last = t_Analisi[2].last = t_Analisi[3].last = \
        t_Analisi[4].last = t_Analisi[5].last = max_value(t_Analisi, t_triage.last, t_queue.last)

    # print("Ci sono state: ", sum(violations), "violazioni su ", analisi_1_volta, "ovvero: ",
    #      (sum(violations) / analisi_1_volta))
    return stat(t_triage, area_triage), stat(t_queue, area_queue), stats(t_Analisi, area_Analisi), batch_res, graph_data


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

    if scegli_azione():
        number_queue += 1
        pass_to_queue(job_completed, queue)
        t_queue.arrival = check_arrival(t_triage.arrival + Parameters.STOP)


def control_job_violation(job_to_control: Job):
    if (job_to_control.get_queue_time() - job_to_control.get_arrival_temp()) > OBIETTIVO[
        job_to_control.get_codice() - 1]:
        violations[job_to_control.get_codice() - 1] += 1
        temp = job_to_control.get_queue_time() - job_to_control.get_arrival_temp() - OBIETTIVO[
            job_to_control.get_codice() - 1]
        violation[job_to_control.get_codice() - 1].append(temp)

        #print("Violazione: ", job_to_control.get_queue_time() - job_to_control.get_arrival_temp() , " Codice: ",  job_to_control.get_codice())


def processa_completamento_queue():
    global index_queue, number_queue, analisi_3_volte, analisi_2_volte, analisi_piu_3, analisi_1_volta, departed_job

    index_queue += 1
    number_queue -= 1
    job_to_analisi = completion_queue(t_queue, servers_busy_queue, queue, area_queue)

    if probability_analisi(job_to_analisi.get_uscita()):
        if job_to_analisi.get_uscita() == 0:
            control_job_violation(job_to_analisi)
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
    else:
        departed_job += 1


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
    global index_triage, index_queue, index_Analisi, departed_job
    t_triage.reset()
    area_triage.reset()
    index_triage = 0
    departed_job = 0

    t_queue.reset()
    area_queue.reset()
    index_queue = 0

    for i in range(len(t_Analisi)):
        t_Analisi[i].reset()
        area_Analisi[i].reset()
        index_Analisi[i] = 0


def scegli_azione():
    global departed_job

    selectStream(3)
    if random() > 0.02:
        return True
    else:
        departed_job += 1
        return False


def monitor_simulation(prox_operazione, stop, printed_status):
    # Calcola le soglie percentuali
    thresholds = {
        "25%": stop * 0.25,
        "50%": stop * 0.50,
        "75%": stop * 0.75,
        "100%": stop
    }

    # Controlla la simulazione e stampa i progressi
    if not printed_status["25%"] and prox_operazione >= thresholds["25%"]:
        print("Raggiunto il 25% della simulazione.")
        printed_status["25%"] = True

    if not printed_status["50%"] and prox_operazione >= thresholds["50%"]:
        print("Raggiunto il 50% della simulazione.")
        printed_status["50%"] = True

    if not printed_status["75%"] and prox_operazione >= thresholds["75%"]:
        print("Raggiunto il 75% della simulazione.")
        printed_status["75%"] = True

    if not printed_status["100%"] and prox_operazione >= thresholds["100%"]:
        print("Raggiunto il 100% della simulazione. \n")
        printed_status["100%"] = True
