from controller.SimulationController import simulation
from utility.SimulationUtils import write_on_csv, confidence_interval
import argparse
from utility.Parameters import *
from utility.Rngs import plantSeeds, DEFAULT

NUMERO_CODICI = 5
NUMERO_ANALISI = 6

RESPONSE_TIME_TRIAGE = []
RESPONSE_TIME_QUEUE = []
DELAY_TIME_QUEUE = []
RESPONSE_TIME_ANALISI = []

RHO_TRIAGE = []
RHO_QUEUE = []
RHO_ANALISI = []

ALPHA = 0.05


def finite(seed, n, stop):
    plantSeeds(seed)
    for i in range(n):

        try:
            stats = simulation(stop)
            response_times_triage, utilization_triage = stats[0][1], stats[0][0]
            response_times_queue, delay_times_queue, utilization_queue = stats[1][1], stats[1][2], stats[1][0]
            response_times_analisi, utilization_analisi = stats[2][1], stats[2][0]
            RESPONSE_TIME_TRIAGE.append(response_times_triage)
            RESPONSE_TIME_QUEUE.append(response_times_queue)
            DELAY_TIME_QUEUE.append(delay_times_queue)
            RESPONSE_TIME_ANALISI.append(response_times_analisi)
            RHO_TRIAGE.append(utilization_triage)
            RHO_QUEUE.append(utilization_queue)
            RHO_ANALISI.append(utilization_analisi)

        except Exception as e:
            print(f"An error occurred during execution: {e}")


def infinite(seed, stop, batch_size=1.0):
    try:
        plantSeeds(seed)
        stats = simulation(stop, batch_size)
        batch_res = stats[3]
        response_times_triage, utilization_triage = batch_res[0][1], batch_res[0][0]
        response_times_queue, delay_times_queue, utilization_queue = batch_res[1][1], batch_res[1][2], batch_res[1][0]
        response_times_analisi, utilization_analisi = batch_res[2][1], batch_res[2][0]

        RESPONSE_TIME_TRIAGE.extend(response_times_triage)
        RESPONSE_TIME_QUEUE.extend(response_times_queue)
        DELAY_TIME_QUEUE.extend(delay_times_queue)
        RESPONSE_TIME_ANALISI.extend(response_times_analisi)

        RHO_TRIAGE.extend(utilization_triage)
        RHO_QUEUE.extend(utilization_queue)
        RHO_ANALISI.extend(utilization_analisi)
        #print(DELAY_TIME_QUEUE)

        write_on_csv(DELAY_TIME_QUEUE)

    except Exception as e:
        print(f"An error occurred during execution: {e}")


def output_finite(n):
    try:
        new_utilization_a = []
        new_response_a = []
        # Itera attraverso la lista originale per estrarre i valori
        for i in range(len(RHO_ANALISI[0])):
            row = [RHO_ANALISI[j][i] for j in range(len(RHO_ANALISI))]
            new_utilization_a.append(row)

        for i in range(len(RESPONSE_TIME_ANALISI[0])):
            row = [RESPONSE_TIME_ANALISI[j][i] for j in range(len(RESPONSE_TIME_ANALISI))]
            new_response_a.append(row)

        response_time_triage = confidence_interval(ALPHA, n, RESPONSE_TIME_TRIAGE)
        utilization_triage = confidence_interval(ALPHA, n, RHO_TRIAGE)
        response_time_queue = confidence_interval(ALPHA, n, RESPONSE_TIME_QUEUE)
        utilization_queue = confidence_interval(ALPHA, n, RHO_QUEUE)
        delay_times_queue = confidence_interval(ALPHA, n, DELAY_TIME_QUEUE)
        response_times_analisi = []
        utilization_analisi = []

        for i in range(len(new_response_a)):
            response_times_analisi.append(confidence_interval(ALPHA, n, new_response_a[i]))
        for i in range(len(new_utilization_a)):
            utilization_analisi.append(confidence_interval(ALPHA, n, new_utilization_a[i]))

        response_a = []
        utilization_a = []
        delay_q = [list(i) for i in zip(*DELAY_TIME_QUEUE)]
        response_q = [list(i) for i in zip(*RESPONSE_TIME_QUEUE)]
        utilization_q = [list(i) for i in zip(*RHO_QUEUE)]
        utilization_t = [list(i) for i in zip(*RHO_TRIAGE)]
        response_t = [list(i) for i in zip(*RESPONSE_TIME_TRIAGE)]
        for j in range(len(new_utilization_a)):
            utilization_a.append([list(i) for i in zip(*new_utilization_a[j])])
        for j in range(len(new_response_a)):
            response_a.append([list(i) for i in zip(*new_response_a[j])])

        for i in range(len(delay_q)):
            print(f"E[Tq] per codice: {i} = {np.mean(delay_q[i])} +/- {delay_times_queue[i]}")
        for i in range(len(response_q)):
            print(f"E[Ts] per codice: {i} = {np.mean(response_q[i])} +/- {response_time_queue[i]}")
        for i in range(len(utilization_q)):
            print(f"E[Rho] per server: {i} = {np.mean(utilization_q[i])} +/- {utilization_queue[i]}")
        for i in range(len(response_t)):
            print(f"E[Ts] per codice: {i} = {np.mean(response_t[i])} +/- {response_time_triage[i]}")
        for i in range(len(utilization_t)):
            print(f"E[Rho] per server: {i} = {np.mean(utilization_t[i])} +/- {utilization_triage[i]}")
        for j in range(len(response_a)):
            for i in range(len(response_a[j])):
                print(f"E[Ts] per codice: {i} = {np.mean(response_a[j][i])} +/- {response_times_analisi[j][i]}")
        for j in range(len(utilization_a)):
            for i in range(len(utilization_a[j])):
                print(f"E[Rho] per server: {i} = {np.mean(utilization_a[j][i])} +/- {utilization_analisi[j][i]}")

    except Exception as e:
        print(f"An error occurred during execution: {e}")


def media_inf(vettore, num_code=7):
    if len(vettore) % num_code != 0:
        raise ValueError("La lunghezza del vettore deve essere divisibile per il numero di colori")
    sottovettori = [[] for _ in range(num_code)]

    for i, valore in enumerate(vettore):
        cod_index = i % num_code
        sottovettori[cod_index].append(valore)

    medie = [np.mean(sottovettore) for sottovettore in sottovettori]

    return medie


def output_infinite():
    media_response_triage = media_inf(RESPONSE_TIME_TRIAGE, num_code=NUMERO_CODICI)
    media_rho_triage = media_inf(RHO_TRIAGE, num_code=NUMERO_DI_SERVER_TRIAGE)
    media_delay_queue = media_inf(DELAY_TIME_QUEUE)
    media_response_queue = media_inf(RESPONSE_TIME_QUEUE)
    media_rho_queue = media_inf(RHO_QUEUE, num_code=NUMERO_DI_SERVER_QUEUE)
    media_response_analisi = media_analisi_inf(RESPONSE_TIME_ANALISI, 6)
    media_rho_analisi = media_analisi_inf(RHO_ANALISI, 6)

    delay_q_vect = suddividi_vettore(DELAY_TIME_QUEUE, 7)
    response_q_vect = suddividi_vettore(RESPONSE_TIME_QUEUE, 7)
    response_t_vect = suddividi_vettore(RESPONSE_TIME_TRIAGE, 5)
    rho_t_vect = suddividi_vettore(RHO_TRIAGE, NUMERO_DI_SERVER_TRIAGE)
    rho_q_vect = suddividi_vettore(RHO_QUEUE, NUMERO_DI_SERVER_QUEUE)

    delay_times_queue = confidence_interval(ALPHA, len(delay_q_vect), delay_q_vect)
    response_time_queue = confidence_interval(ALPHA, len(response_q_vect), response_q_vect)
    utilization_queue = confidence_interval(ALPHA, len(rho_q_vect), rho_q_vect)
    utilization_triage = confidence_interval(ALPHA, len(rho_t_vect), rho_t_vect)
    response_time_triage = confidence_interval(ALPHA, len(response_t_vect), response_t_vect)

    new_utilization_a = []
    new_response_a = []
    utilizations_analisi = suddividi_vettore_analisi(RHO_ANALISI, 6)
    response_analisi = suddividi_vettore_analisi(RESPONSE_TIME_ANALISI, 6)

    # Itera attraverso la lista originale per estrarre i valori
    for i in range(len(utilizations_analisi[0])):
        row = [utilizations_analisi[j][i] for j in range(len(utilizations_analisi))]
        new_utilization_a.append(row)

    for i in range(len(response_analisi[0])):
        row = [response_analisi[j][i] for j in range(len(response_analisi))]
        new_response_a.append(row)

    response_times_analisi = []
    utilization_analisi = []

    for i in range(len(new_response_a)):
        response_times_analisi.append(confidence_interval(ALPHA, len(new_response_a[i]), new_response_a[i]))
    for i in range(len(new_utilization_a)):
        utilization_analisi.append(confidence_interval(ALPHA, len(new_utilization_a[i]), new_utilization_a[i]))

    for i in range(len(media_delay_queue)):
        print(f"E[Tq] per codice: {i} = {media_delay_queue[i]} +/- {delay_times_queue[i]}")
    for i in range(len(media_response_queue)):
        print(f"E[Ts] per codice: {i} = {media_response_queue[i]} +/- {response_time_queue[i]}")
    for i in range(len(media_rho_queue)):
        print(f"E[Rho] per server: {i} = {media_rho_queue[i]} +/- {utilization_queue[i]}")
    for i in range(len(media_response_triage)):
        print(f"E[Ts] per codice: {i} = {media_response_triage[i]} +/- {response_time_triage[i]}")
    for i in range(len(media_rho_triage)):
        print(f"E[Rho] per server: {i} = {media_rho_triage[i]} +/- {utilization_triage[i]}")

    for j in range(len(media_response_analisi)):
        for i in range(len(media_response_analisi[j])):
            print(f"E[Ts] per codice: {i} = {media_response_analisi[j][i]} +/- {response_times_analisi[j][i]}")
    for j in range(len(media_rho_analisi)):
        for i in range(len(media_rho_analisi[j])):
            print(f"E[Rho] per server: {i} = {media_rho_analisi[j][i]} +/- {utilization_analisi[j][i]}")

def suddividi_vettore(vettore, n_elementi):
    if len(vettore) % n_elementi != 0:
        raise ValueError("La lunghezza del vettore non è divisibile per il numero di elementi per sottovettore.")

    sottovettori = [vettore[i:i + n_elementi] for i in range(0, len(vettore), n_elementi)]
    return sottovettori


def suddividi_vettore_analisi(vettore, n_elementi):
    if len(vettore) % n_elementi != 0:
        raise ValueError("La lunghezza del vettore non è divisibile per il numero di elementi per sottovettore.")

    sottovettori = [vettore[i:i + n_elementi] for i in range(0, len(vettore), n_elementi)]
    return sottovettori


def trasforma_analisi(vettori, n_gruppi):
    # Inizializza le liste per raccogliere gli elementi delle diverse posizioni nei gruppi
    gruppi = [[] for _ in range(n_gruppi)]

    # Distribuisci i vettori nei rispettivi gruppi
    for i, vettore in enumerate(vettori):
        gruppo_idx = i % n_gruppi
        gruppi[gruppo_idx].append(vettore)

    return gruppi


def media_analisi_inf(vettori, n_gruppi):
    gruppi = trasforma_analisi(vettori, n_gruppi)
    # Calcola la media per ciascuna posizione nei gruppi
    medie = []
    for gruppo in gruppi:
        medie_gruppo = np.mean(gruppo, axis=0)
        medie.append(medie_gruppo)

    return medie


if __name__ == "__main__":
    batch_size = 940
    #
    parser = argparse.ArgumentParser(description="Scelta modalità di simulazione")
    parser.add_argument('-m', '--modality', type=str, help="Inserire -m finite per simulazione finita, lasciare vuoto "
                                                           "per infinita")
    parser.add_argument('-r', '--repetition', type=int, help="Inserire -m seguito da un intero per inserire il "
                                                             "numero di ripetizioni")

    args = parser.parse_args()

    # Utilizza le flag e gli argomenti
    if args.modality == "finite":

        if args.repetition is not None and args.repetition > 0:
            print("Eseguo", args.repetition, "ripetizioni")
        else:
            raise Exception("Numero di ripetizioni per simulazione ad orizzonte finito <= 0")

        print("Inizio simulazione ad orizzonte finito... ")
        finite(DEFAULT, args.repetition, STOP)
        output_finite(args.repetition)

    elif (args.modality is None or args.modality == "infinite") and args.repetition is None:
        print("Inizio simulazione ad orizzonte infinito... ")
        infinite(DEFAULT, STOP, batch_size)
        output_infinite()
    else:
        raise Exception("Argomento dei flag non valido")

#    if sys.argv[2] == "finite":
#
#
#    elif sys.argv[2] == "infinite":
#        stop = 2000000.0
#        batch_size = 128
#
#        infinite(SEED, stop, batch_size=batch_size)
#
#        # response_time_monitor_mean: Provided no points are discarded,                                           */
#        # the “mean of the means” is the same as the “grand sample mean”                                          */
#        response_time_monitor_mean = np.mean(RESPONSE_TIME_MONITOR)
#        response_time_monitor_interval = confidence_interval(ALPHA, len(RESPONSE_TIME_MONITOR), RESPONSE_TIME_MONITOR)
#
#        response_time_monitor1_mean = np.mean(RESPONSE_TIME_MONITOR1)
#        response_time_monitor1_interval = confidence_interval(ALPHA, len(RESPONSE_TIME_MONITOR1),
#                                                              RESPONSE_TIME_MONITOR1)
#
#        waiting_time_monitor_mean = np.mean(WAITING_TIME_MONITOR)
#        waiting_time_monitor_interval = confidence_interval(ALPHA, len(WAITING_TIME_MONITOR), WAITING_TIME_MONITOR)
#
#        response_time_plan_mean = np.mean(RESPONSE_TIME_PLAN)
#        response_time_plan_interval = confidence_interval(ALPHA, len(RESPONSE_TIME_PLAN), RESPONSE_TIME_PLAN)
#
#        waiting_time_plan_mean = np.mean(WAITING_TIME_PLAN)
#        waiting_time_plan_interval = confidence_interval(ALPHA, len(WAITING_TIME_PLAN), WAITING_TIME_PLAN)
#
#        rho_man1_mean = np.mean(RHO_MONITOR_1)
#        rho_man1_interval = confidence_interval(ALPHA, len(RHO_MONITOR_1), RHO_MONITOR_1)
#        rho_man2_mean = np.mean(RHO_MONITOR_2)
#        rho_man2_interval = confidence_interval(ALPHA, len(RHO_MONITOR_2), RHO_MONITOR_2)
#        rho_man3_mean = np.mean(RHO_MONITOR_3)
#        rho_man3_interval = confidence_interval(ALPHA, len(RHO_MONITOR_3), RHO_MONITOR_3)
#        rho_plan_mean = np.mean(RHO_PLAN)
#        rho_plan_interval = confidence_interval(ALPHA, len(RHO_PLAN), RHO_PLAN)
#
#        print("Monitor Centre")
#        print(f"E[Tq] = {waiting_time_monitor_mean} +/- {waiting_time_monitor_interval}")
#        print(f"E[Ts] = {response_time_monitor_mean} +/- {response_time_monitor_interval}")
#        print(f"E[Ts1] = {response_time_monitor1_mean} +/- {response_time_monitor1_interval}")
#        print(f"rho_1 = {rho_man1_mean} +/- {rho_man1_interval}")
#        print(f"rho_2 = {rho_man2_mean} +/- {rho_man2_interval}")
#        print(f"rho_3 = {rho_man3_mean} +/- {rho_man3_interval}")
#
#        print("Plan Centre")
#        print(f"E[Tq] = {waiting_time_plan_mean} +/- {waiting_time_plan_interval}")
#        print(f"E[Ts] = {response_time_plan_mean} +/- {response_time_plan_interval}")
#        print(f"rho = {rho_plan_mean} +/- {rho_plan_interval}")
#
#        # Compute cumulative means
#        cumulative_response_time_monitor = cumulative_mean(RESPONSE_TIME_MONITOR)
#        cumulative_response_time1_monitor = cumulative_mean(RESPONSE_TIME_MONITOR1)
#        cumulative_waiting_time_monitor = cumulative_mean(WAITING_TIME_MONITOR)
#        cumulative_response_time_plan = cumulative_mean(RESPONSE_TIME_PLAN)
#        cumulative_waiting_time_plan = cumulative_mean(WAITING_TIME_PLAN)
#
#        # Plot for QoS1
#        values = (np.array(cumulative_response_time_monitor) + np.array(cumulative_response_time_plan)).tolist()
#        plots.plot_qos1_base(values)
#
#        # Plot for QoS2
#        min_length = min(len(cumulative_response_time1_monitor), len(cumulative_response_time_plan))
#        array1 = np.array(cumulative_response_time1_monitor[:min_length])
#        array2 = np.array(cumulative_response_time_plan[:min_length])
#        values = (np.array(array1) + np.array(array2)).tolist()
#        plots.plot_qos2_base(values)
#
#        # Plot cumulative means for Monitor area
#        plot_cumulative_means(cumulative_response_time_monitor, response_time_monitor_mean,
#                              'Cumulative Mean Response Time (Monitor)',
#                              'Cumulative Mean Response Time over Batches (Monitor Centre)',
#                              'cumulative_response_time_monitor')
#        plot_cumulative_means(cumulative_response_time1_monitor, response_time_monitor1_mean,
#                              'Cumulative Mean Response Time 1 (Monitor)',
#                              'Cumulative Mean Response Time 1 over Batches (Monitor Centre)',
#                              'cumulative_response_time1_monitor')
#        plot_cumulative_means(cumulative_waiting_time_monitor, waiting_time_monitor_mean,
#                              'Cumulative Mean Waiting Time (Monitor)',
#                              'Cumulative Mean Waiting Time over Batches (Monitor Centre)',
#                              'cumulative_waiting_time_monitor')
#
#        # Plot cumulative means for Plan area
#        plot_cumulative_means(cumulative_response_time_plan, response_time_plan_mean,
#                              'Cumulative Mean Response Time (Plan)',
#                              'Cumulative Mean Response Time over Batches (Plan Centre)',
#                              'cumulative_response_time_plan')
#        plot_cumulative_means(cumulative_waiting_time_plan, waiting_time_plan_mean,
#                              'Cumulative Mean Waiting Time (Plan)',
#                              'Cumulative Mean Waiting Time over Batches (Plan Centre)', 'cumulative_waiting_time_plan')
#
#    else:
#        print("Usage: python originalmain.py <number_of_times> [finite | infinite]")
#        sys.exit(1)
