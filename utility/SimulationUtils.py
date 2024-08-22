from utility.rvms import idfStudent
import numpy as np
import csv
import os
import matplotlib.pyplot as plt
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
        utilization.append((area.service[j] - service[j]) / (t.current - current) if t.current > 0 else 0)
    for i in range(len(area.jobs_complete_color)):
        if (area.jobs_complete_color[i] - jobs_complete[i]) != 0:
            response_time.append((area.wait_time[i] - wait_time[i]) / (area.jobs_complete_color[i] - jobs_complete[i]))
            delay_time.append((area.delay_time[i] - delay_times[i]) / (area.jobs_complete_color[i] - jobs_complete[i]))

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
