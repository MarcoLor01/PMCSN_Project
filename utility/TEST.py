# # -------------------------------------------------------------------------
#  * This program is a next-event simulation of a single-server FIFO service
#  * node using Exponentially distributed interarrival times and Uniformly
#  * distributed service times (i.e., an M/U/1 queue).  The service node is
#  * assumed to be initially idle, no arrivals are permitted after the
#  * terminal time STOP, and the service node is then purged by processing any
#  * remaining jobs in the service node.
#  *
#  * Name            : ssq3.c  (Single Server Queue, version 3)
#  * Author          : Steve Park & Dave Geyer
#  * Language        : ANSI C
#  * Latest Revision : 10-19-98
#  # Translated by   : Philip Steele
#  # Language        : Python 3.3
#  # Latest Revision : 3/26/14
#  * -------------------------------------------------------------------------
#  */

import csv
from math import log
import matplotlib
from matplotlib import pyplot as plt
from rngs import plantSeeds, random, selectStream, getSeed
from rngs import DEFAULT

matplotlib.use('TkAgg')
NUMBER_SIMULATION = 5
START = 0.0  # initial time                   */
STOP = 2000000.0  # terminal (close the door) time */
INFINITY = (100.0 * STOP)  # must be much larger than STOP  */
arrivalTemp = START  # global temp var for getArrival function
summary = 0
iteration = 0
file_csv = "metrics.csv"
matrix = []
max_simulation = 2000000
step_size = 500
plantSeeds(DEFAULT)


def Min(a, c):
    # ------------------------------
    # * return the smaller of a, b
    # * ------------------------------
    # */
    if a < c:
        return a
    else:
        return c


def Exponential(m):
    # ---------------------------------------------------
    # * generate an Exponential random variate, use m > 0.0
    # * ---------------------------------------------------
    # */
    return -m * log(1.0 - random())


def Uniform(a, b):
    # --------------------------------------------
    # * generate a Uniform random variate, use a < b
    # * --------------------------------------------
    # */
    return a + (b - a) * random()


def GetArrival():
    # ---------------------------------------------
    # * generate the next arrival time, with rate 1/2
    # * ---------------------------------------------
    # */
    global arrivalTemp
    selectStream(0)
    arrivalTemp += Exponential(2)
    return arrivalTemp


def GetService():
    # --------------------------------------------
    # * generate the next service time with rate 1/2
    # * --------------------------------------------
    # */

    selectStream(100)
    return Uniform(1, 2)


def Feedback():
    selectStream(200)
    p_feedback = 0.2
    if random() < p_feedback:
        return True
    else:
        return False


class track:
    node = 0.0  # time integrated number in the node  */
    queue = 0.0  # time integrated number in the queue */
    service = 0.0  # time integrated number in service   */


class time:
    arrival = -1  # next arrival time                   */
    completion = -1  # next completion time                */
    current = -1  # current time                        */
    next = -1  # next (most imminent) event time     */
    last = -1  # last arrival time                   */


def Reset():
    global arrivalTemp, t, area, matrix
    arrivalTemp = START
    t.current = START  # set the clock                         */
    t.completion = INFINITY  # the first event can't be a completion */
    area.node = 0
    area.queue = 0
    area.service = 0
    matrix.clear()


def Simulation():
    index = 0  # used to count departed jobs         */
    number = 0  # number in the node                  */
    job_feedback = 0
    t.arrival = GetArrival()  # schedule the first arrival            */
    while (t.arrival < STOP) or (number > 0):
        t.next = Min(t.arrival, t.completion)  # next event time   */
        if number > 0:  # update integrals  */
            area.node += (t.next - t.current) * number
            area.queue += (t.next - t.current) * (number - 1)
            area.service += (t.next - t.current)
        # EndIf

        t.current = t.next  # advance the clock */

        if t.current == t.arrival:  # process an arrival */

            number += 1
            t.arrival = GetArrival()
            if t.arrival > STOP:
                t.last = t.current
                t.arrival = INFINITY

            if number == 1:
                t.completion = t.current + GetService()
        # EndOuterIf
        else:  # process a completion */
            index += 1
            if not Feedback():
                number -= 1
            else:
                job_feedback += 1
            if number > 0:
                t.completion = t.current + GetService()
            else:
                t.completion = INFINITY
            if index % step_size == 0 and index < max_simulation and index != 0:
                SaveData(index)
            # EndWhile
    print("   average interarrival time = {0:6.2f}".format(t.last / (index-job_feedback)))
    print("   average wait ............ = {0:6.2f}".format(area.node / (index-job_feedback)))
    print("   average delay ........... = {0:6.2f}".format(area.queue / (index-job_feedback)))
    print("   average service time .... = {0:6.2f}".format(area.service / (index-job_feedback)))
    print("   average # in the node ... = {0:6.2f}".format(area.node / t.current))
    print("   average # in the queue .. = {0:6.2f}".format(area.queue / t.current))
    print("   utilization ............. = {0:6.2f}".format(area.service / t.current))



def SaveData(index):
    average_wait = area.node / index
    average_in_node = area.node / t.current
    average_in_queue = area.queue / t.current
    utilization = area.service / t.current
    matrix.append([index, average_wait, average_in_node, average_in_queue, utilization])


def CleanData():
    with open(file_csv, mode='w', newline='') as file:
        pass


def WriteData():
    with open(file_csv, mode='a', newline='') as file:
        writer = csv.writer(file)
        for row in matrix:
            writer.writerow(row)
        writer.writerow(['Delimiter'])


def GraphicData(metric, metricsrow, seed):
    x = []
    y = []
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
    color_index = 0

    with open(file_csv, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row == ['Delimiter']:
                if x and y:
                    plt.scatter(x, y, color=colors[color_index % len(colors)], label=f'Seed: {seed[color_index]}', s=6)
                    color_index += 1
                    x = []
                    y = []
            else:
                x.append(float(row[0]))
                y.append(float(row[metricsrow]))

    # Plot any remaining points after the last delimiter
    if x and y:
        plt.scatter(x, y, color=colors[color_index % len(colors)], label=f'Seed: {seed[color_index + 1]}', s=6)

    plt.xlabel('Number of Jobs')
    plt.ylabel(metric)
    plt.title("Metric Graphic")
    plt.grid(True)
    plt.legend()
    plt.show()


area = track()
t = time()


def main():
    seeds = []
    CleanData()
    i = 0
    while i < NUMBER_SIMULATION:
        seed = getSeed()
        Reset()
        Simulation()
        seeds.append(seed)
        WriteData()
        i += 1
    GraphicData("Waiting Time", 1, seeds)
    GraphicData("Utilization", 4, seeds)
    GraphicData("Average in the Queue", 3, seeds)


if __name__ == "__main__":
    main()