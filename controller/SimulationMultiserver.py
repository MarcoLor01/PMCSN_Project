from utility.CodeEnum import Code
from utility.Parameters import *
from utility.Rngs import selectStream, plantSeeds
from utility.Rngs import DEFAULT
from utility.Rvgs import Exponential, Lognormal
from model.Job import Job
from utility.ArrivalService import *
from utility.Utils import Minimum

summary = 0
max_simulation = 2000000
step_size = 500
iteration = 0
arrivalTemp = START  # global temp var for getArrival function

plantSeeds(DEFAULT)

class Track:
    node = 0.0  # time integrated number in the node
    queue = 0.0  # time integrated number in the queue
    service = 0.0  # time integrated number in service

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

def GetNextJobToServe(queue):
    """Selects the next job to serve based on a scheduling policy"""
    if queue:
        return queue.pop(0)  # Simple FIFO (First In, First Out) policy
    else:
        return None

def Simulation():
    global arrivalTemp
    index = 0  # used to count departed jobs
    number = 0  # number of jobs in the system
    servers_busy = [False] * NUMERO_DI_SERVER  # track busy/free status of servers
    queue = []  # queue for jobs waiting to be served

    arrivalTemp = arrivalTemp + GetArrival()
    t.arrival = arrivalTemp  # schedule the first arrival

    while (t.arrival < STOP) or (number > 0):
        min_completion, server_index = MinTimeCompletion(t.completion + [INFINITY])  # include INFINITY for queue check
        t.next = Minimum(t.arrival, min_completion)  # next event time

        if number > 0:  # update integrals
            area.node += (t.next - t.current) * number
            area.queue += (t.next - t.current) * (number - sum(servers_busy))
            area.service += (t.next - t.current) * sum(servers_busy)

        t.current = t.next  # advance the clock

        if t.current == t.arrival:  # process an arrival
            number += 1
            job = Job(arrivalTemp)
            queue.append(job)
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

            job_to_serve = GetNextJobToServe(queue)
            if job_to_serve:
                servers_busy[server_index] = True
                t.completion[server_index] = t.current + GetServiceTriage()

    print("   average interarrival time = {0:6.2f}".format(t.last / index))
    print("   average wait ............ = {0:6.2f}".format(area.node / index))
    print("   average delay ........... = {0:6.2f}".format(area.queue / index))
    print("   average service time .... = {0:6.2f}".format(area.service / index))
    print("   average # in the node ... = {0:6.2f}".format(area.node / t.current))
    print("   average # in the queue .. = {0:6.2f}".format(area.queue / t.current))
    print("   utilization ............. = {0:6.2f}".format(area.service / t.current))

area = Track()
t = Time()

def main():
    Simulation()

if __name__ == "__main__":
    main()



###QUI VA INTEGRATO IL MULTISERVER, COSA CHE ADESSO NON SONO RIUSCITO
# A FAR FUNZIONARE IL VECCHIO CONTROLLER MA è A SERVENTE UNICO
# POSSIAMO FARCI I CONTI IN MANIERA ANALITICA PER VERIFIACRE E FAR FUNZIONARE QUESTO,
# POI IL 90% DEL LAVORO DOVREBBE ESSERE FATTO
