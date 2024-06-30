from controller.TriageController import giveCode
from utility.ArrivalService import *
from utility.Utils import Minimum
import logging

# Configurazione del logger
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

summary = 0
max_simulation = 2000000
step_size = 500
iteration = 0
arrivalTemp = START  # global temp var for getArrival function

plantSeeds(DEFAULT)


class Track:
    node = 0.0  # time integrated number in the node
    queue = 0.0  # time integrated number in the queue
    service = [0.0] * NUMERO_DI_SERVER  # time integrated number in service
    jobs_completed = [0] * NUMERO_DI_SERVER
    wait_time = [0.0] * 5
    jobs_complete_color = [0] * 5
class Time:
    arrival = -1  # next arrival time
    completion = [-1] * NUMERO_DI_SERVER  # next completion times for each server
    current = -1  # current time
    next = -1  # next (most imminent) event time
    last = -1  # last arrival time


def MinTimeCompletion(completion_times):
    """Returns the minimum completion time and the index of the server"""
    min_completion_time = min(completion_times)
    min_index = completion_times.index(min_completion_time)
    return min_completion_time, min_index


def GetNextJobToServe(list_of_queues):
    """Selects the next job to serve based on a priority policy"""
    for queue in list_of_queues:
        if queue:
            return queue.pop(0)  # Simple FIFO (First In, First Out) policy for each priority queue
    return None


def add_job_to_queue(job, queue):
    index = job.getCodice() - 1  # Utilizza getCodice per determinare l'indice della lista
    if 0 <= index < len(queue):
        queue[index].append(job)
    else:
        print(f"Index {index} is out of range for list_of_queues")


def Simulation():
    global arrivalTemp
    queueRed = []
    queueOrange = []
    queueBlue = []
    queueGreen = []
    queueWhite = []
    queue = [queueRed, queueOrange, queueBlue, queueGreen, queueWhite]  # queue for jobs waiting to be served divided for colors

    index = 0  # used to count departed jobs
    number = 0  # number of jobs in the system
    servers_busy = [False] * NUMERO_DI_SERVER  # track busy/free status of servers
    arrivalTemp = START
    t.current = START  # set the clock
    for i in range(NUMERO_DI_SERVER):
        t.completion[i] = INFINITY  # the first event can't be a completion */
        area.service[i] = 0
    for i in range(5):
        area.wait_time[i] = 0
        area.jobs_complete_color[i] = 0
    area.node = 0
    area.queue = 0

    arrivalTemp = arrivalTemp + GetArrival()
    t.arrival = arrivalTemp  # schedule the first arrival

    while (t.arrival < STOP) or (number > 0):
        min_completion, server_index = MinTimeCompletion(t.completion + [INFINITY])  # include INFINITY for queue check
        t.next = Minimum(t.arrival, min_completion)  # next event time

        if number > 0:
            area.node += (t.next - t.current) * number
            area.queue += (t.next - t.current) * (number - sum(servers_busy))
            for i in range(NUMERO_DI_SERVER):
                area.service[i] = area.service[i] + (t.next - t.current) * servers_busy[i]


        t.current = t.next  # advance the clock

        if t.current == t.arrival:  # process an arrival
            number += 1
            job = Job(arrivalTemp)
            job.triage(giveCode())
            add_job_to_queue(job, queue)
            arrivalTemp = arrivalTemp + GetArrival()
            t.arrival = arrivalTemp

            if t.arrival > STOP:
                t.last = t.current
                t.arrival = INFINITY

            for i in range(NUMERO_DI_SERVER):
                if not servers_busy[i]:  # check if server is free
                    job_to_serve = GetNextJobToServe(queue)
                    if job_to_serve:
                        servers_busy[i] = True
                        t.completion[i] = t.current + GetServiceTriage()
                        break

        else:  # process a completion
            index += 1
            number -= 1
            servers_busy[server_index] = False
            t.completion[server_index] = INFINITY
            area.jobs_completed[server_index] += 1

            job_to_serve = GetNextJobToServe(queue)

            if job_to_serve:
                #print("Sto lavorando il job:", job_to_serve.getArrivalTemp())
                #print("Ha codice: ", job_to_serve.getCodice())
                servers_busy[server_index] = True
                t.completion[server_index] = t.current + GetServiceTriage()
                area.wait_time[job_to_serve.getCodice()-1] += t.current - job_to_serve.getArrivalTemp()
                area.jobs_complete_color[job_to_serve.getCodice()-1] += 1

    logger.info(f"Average interarrival time: {t.last / sum(area.jobs_completed):.2f}")
    logger.info(f"Average wait: {area.node / sum(area.jobs_completed):.2f}")
    logger.info(f"Average delay: {area.queue / sum(area.jobs_completed):.2f}")
    logger.info(f"Average service time: {sum(area.service) / sum(area.jobs_completed):.2f}")
    logger.info(f"Average number in the node: {area.node / t.current:.2f}")
    logger.info(f"Average number in the queue: {area.queue / t.current:.2f}")

    for i in range(NUMERO_DI_SERVER):
        utilization = area.service[i] / t.current if t.current > 0 else 0
        avg_service_time = area.service[i] / area.jobs_completed[i] if area.jobs_completed[i] > 0 else 0

        logger.info(f"Utilization of server {i + 1}: {utilization:.2f}")
        logger.info(f"Average service time of server {i + 1}: {avg_service_time:.2f}")
    for i in range(5):
        logger.info(f"Waiting time for color {i + 1}: {area.wait_time[i]}")
        logger.info(f"job for color {i + 1}: {area.jobs_complete_color[i]}")
        logger.info(f"Attesa media {i + 1}: {area.wait_time[i]/area.jobs_complete_color[i]}")


area = Track()
t = Time()


def main():
    Simulation()


if __name__ == "__main__":
    main()

