import sys
from controller.SimulationController import simulation
from utility.SimulationUtils import write_on_csv, confidence_interval
import argparse
import numpy as np
import csv
import os
import matplotlib.pyplot as plt
from utility.Parameters import *
from utility.Rngs import plantSeeds, DEFAULT

NUMERO_CODICI = 5
NUMERO_ANALISI = 7

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

        write_on_csv(DELAY_TIME_QUEUE)

    except Exception as e:
        print(f"An error occurred during execution: {e}")


def output_finite(n):
    try:
        response_time_triage = confidence_interval(ALPHA, n, RESPONSE_TIME_TRIAGE)
        utilization_triage = confidence_interval(ALPHA, n, RHO_TRIAGE)
        response_time_queue = confidence_interval(ALPHA, n, RESPONSE_TIME_QUEUE)
        utilization_queue = confidence_interval(ALPHA, n, RHO_QUEUE)
        delay_times_queue = confidence_interval(ALPHA, n, DELAY_TIME_QUEUE)
        response_times_analisi = []
        utilization_analisi = []
        #print("Rpt: ", RESPONSE_TIME_TRIAGE)
        #print("RPT: ", response_time_triage)

        for i in range(len(RESPONSE_TIME_ANALISI)):
            response_times_analisi.append(confidence_interval(ALPHA, n, RESPONSE_TIME_ANALISI[i]))
            utilization_analisi.append(confidence_interval(ALPHA, n, RHO_ANALISI[i]))
        delay_t = [list(i) for i in zip(*DELAY_TIME_QUEUE)]


        for i in range(len(delay_t)):
            print(f"E[Tq] per codice: {i} = {np.mean(delay_t[i])} +/- {delay_times_queue[i]}")

    #       print(f"E[Ts] = {np.mean(RESPONSE_TIME_MONITOR)} +/- {response_time_monitor_interval}")
    #       print(f"E[Ts1] = {np.mean(RESPONSE_TIME_MONITOR1)} +/- {response_time_monitor1_interval}")
    #       print(f"rho1 = {np.mean(RHO_MONITOR_1)} +/- {rho_man1_interval}")
    #       print(f"rho2 = {np.mean(RHO_MONITOR_2)} +/- {rho_man2_interval}")
    #       print(f"rho3 = {np.mean(RHO_MONITOR_3)} +/- {rho_man3_interval}")
    #               print("Plan Centre")
    #       print(f"E[Tq] = {np.mean(WAITING_TIME_PLAN)} +/- {waiting_time_plan_interval}")
    #       print(f"E[Ts] = {np.mean(RESPONSE_TIME_PLAN)} +/- {response_time_plan_interval}")
    #       print(f"rho = {np.mean(RHO_PLAN)} +/- {rho_pla_interval}")
    except Exception as e:
        print(f"An error occurred during execution: {e}")


def output_infinite():
    pass


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
