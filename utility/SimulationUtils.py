from typing import Tuple, List, Any

from utility.rvms import idfStudent
import numpy as np
import csv
import os
import matplotlib.pyplot as plt
from utility.Parameters import *
from utility.Utils import *


def confidence_interval(alpha, n, l):
    res = []
    l_t = [list(i) for i in zip(*l)]
    for i in range(len(l_t)):
        res.append(confidence_interval_iteration(alpha, n, l_t[i]))
    return res


def confidence_interval_iteration(alpha, n, l):
    sigma = np.std(l, ddof=1)
    if n > 1:
        t = idfStudent(n - 1, 1 - alpha / 2)
        return (t * sigma) / np.sqrt(n - 1)
    else:
        return 0.0


def batch_means(data, batch_size):
    n = len(data)
    num_batches = n // batch_size
    batch_means = []

    for i in range(num_batches):
        batch = data[i * batch_size: (i + 1) * batch_size]
        batch_means.append(np.mean(batch))

    return batch_means


def write_on_csv(input_list):
    with open("acs.dat", mode='w', newline='') as file:
        writer = csv.writer(file)
        for element in input_list:
            writer.writerow([element])


def cumulative_mean(data):
    # Computes the cumulative mean for an array of data
    return np.cumsum(data) / np.arange(1, len(data) + 1)


def plot_cumulative_means(cumulative_means, stationary_value, ylabel, title, filename):
    plt.figure(figsize=(10, 6))
    plt.plot(cumulative_means, label=ylabel)
    plt.xlabel('Batch Number')

    # Plot a horizontal line for the stationary value
    plt.axhline(stationary_value, color='orange', label='Mean of means')

    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
    plt.grid(True)

    # Create folder 'plots' if it doesn't exist
    if not os.path.exists('plots'):
        os.makedirs('plots')

    # Save plots
    plt.savefig(f'plots/{filename}.png')
    plt.close()


def plot_cumulative_and_qos(qos, cumulative_values, x_label, y_label, title, filename, label_values, label_qos):
    # Dati da plottare
    x = np.arange(len(cumulative_values))
    y = cumulative_values

    # Creazione del plot
    plt.figure(figsize=(9, 5))  # Dimensioni del plot (larghezza, altezza)
    plt.plot(x, y, label=label_values)  # Plot dei dati con linea e marker
    plt.axhline(y=qos, color='r', label=label_qos)
    plt.title(title)  # Titolo del grafico
    plt.xlabel(x_label)  # Etichetta dell'asse X
    plt.ylabel(y_label)  # Etichetta dell'asse Y
    plt.grid(True)  # Mostra griglia
    plt.legend()  # Mostra legenda
    # Salvataggio del plot come immagine PNG
    plt.savefig('plots/' + filename + '.png')


#_______________QoS1 base________________________________________________________________
def plot_qos1_base(value_list):
    print("Plotting QoS 1 base")
    qos = 0.5
    # Values: Global mean response times (Base)
    cumulative_values = value_list
    x_label = 'Batch Number'
    y_label = 'Cumulative response time value (s)'
    title = 'QoS1: Cumulative global mean response time (Base System)'
    filename = 'qos1_response_time_base'
    label_values = 'Cumulative global mean response time'
    label_qos = 'QoS1: Response time'
    plot_cumulative_and_qos(qos, cumulative_values, x_label, y_label, title, filename, label_values, label_qos)


#________________QoS2 base______________________________________________________________
def plot_qos2_base(value_list):
    qos = 0.0019320729
    # Values: Fatal mean response times (Base)
    cumulative_values = value_list
    x_label = 'Batch Number'
    y_label = 'Cumulative response time value (s)'
    title = 'QoS2: Cumulative mean response time for Web server logs (Base System)'
    filename = 'qos2_response_time_1_base'
    label_values = 'Cumulative Mean response time for Web server logs'
    label_qos = 'QoS2: Response time'
    plot_cumulative_and_qos(qos, cumulative_values, x_label, y_label, title, filename, label_values, label_qos)


#______________________________QoS1 better______________________________________________
def plot_qos1_better(value_list):
    qos = 0.5
    # Values: Global mean response times (Better)
    cumulative_values = value_list
    x_label = 'Batch Number'
    y_label = 'Cumulative response time value (s)'
    title = 'QoS1: Cumulative global mean response time (Better System)'
    filename = 'qos1_response_time_better'
    label_values = 'Cumulative global mean response time'
    label_qos = 'QoS1: Response time'
    plot_cumulative_and_qos(qos, cumulative_values, x_label, y_label, title, filename, label_values, label_qos)


#_____________________________QoS2 better__________________________________________________
def plot_qos2_better(value_list):
    qos = 0.0019320729
    # Values:Fatal mean response times (Better)
    cumulative_values = value_list
    x_label = 'Batch Number'
    y_label = 'Cumulative response time value (s)'
    title = 'QoS2: Cumulative mean response time for Web server logs (Better System)'
    filename = 'qos2_response_time_1_better'
    label_values = 'Cumulative Mean response time for Web server logs'
    label_qos = 'QoS2: Response time'
    plot_cumulative_and_qos(np.mean(value_list), cumulative_values, x_label, y_label, title, filename, label_values,
                            label_qos)


def stat(t: Time, area: Track) -> tuple[list[float], list[float], list[float]]:
    utilization = []
    response_time = []
    delay_time = []

    for j in range(len(area.service)):
        utilization.append(area.service[j] / t.last if t.last > 0 else 0)
    for i in range(len(area.jobs_complete_color)):
        if area.jobs_complete_color[i] != 0:
            response_time.append(area.wait_time[i] / area.jobs_complete_color[i])
            delay_time.append(area.delay_time[i] / area.jobs_complete_color[i])

    return utilization, response_time, delay_time


def stats(t: list, area: list):
    utilizations = []
    response_times = []
    delay_times = []
    for i in range(len(t)):
        u, w, d = stat(t[i], area[i])
        utilizations.append(u)
        response_times.append(w)
        delay_times.append(d)

    return utilizations, response_times, delay_times


def stat_batch(t: Time, area: Track, service, current, jobs_complete, wait_time, delay_times) -> tuple[
    list[float], list[float], list[float]]:
    utilization = []
    response_time = []
    delay_time = []

    for j in range(len(area.service)):
        #print("AREA.SERVICE: ", area.service[j], "SERVICE: ", service[j])
        utilization.append((area.service[j] - service[j]) / (t.current - current) if t.current > 0 else 0)
    for i in range(len(area.jobs_complete_color)):
        if (area.jobs_complete_color[i] - jobs_complete[i]) != 0:
            response_time.append((area.wait_time[i] - wait_time[i]) / (area.jobs_complete_color[i] - jobs_complete[i]))
            delay_time.append((area.delay_time[i] - delay_times[i]) / (area.jobs_complete_color[i] - jobs_complete[i]))
    #print("UTILIZATION: ", utilization)

    return utilization, response_time, delay_time


def stats_batch(t: list, area: list, service, current, jobs_complete, wait_time, delay_time):
    utilization = []
    response_times = []
    delay_times = []
    for i in range(len(t)):
        u, w, d = stat_batch(t[i], area[i], service[i], current, jobs_complete[i], wait_time[i], delay_time[i])
        utilization.append(u)
        response_times.append(w)
        delay_times.append(d)

    return utilization, response_times, delay_times
