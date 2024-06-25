from utility.CodeEnum import Code
from utility.Parameters import *
from utility.Rngs import selectStream, plantSeeds
from utility.Rngs import DEFAULT
from utility.Rvgs import Exponential, Lognormal
from model.Job import Job

summary = 0
max_simulation = 2000000
step_size = 500
iteration = 0
arrivalTemp = START  # global temp var for getArrival function

plantSeeds(DEFAULT)


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


def GetArrival():
    # ---------------------------------------------
    # * generate the next arrival time, with rate 1/2
    # * ---------------------------------------------
    # */
    global arrivalTemp
    selectStream(0)
    arrivalTemp += Exponential(1 / TASSO_DI_INGRESSO)  # Lavoriamo su job al minuto
    newJob = Job(int(arrivalTemp))
    return newJob


def GetServiceTriage():
    # --------------------------------------------
    # * generate the next service time with rate 1/2
    # * --------------------------------------------
    # */
    selectStream(2)
    return Lognormal(MEDIA_DI_SERVIZIO_TRIAGE, VARIANZA_DI_SERVIZIO_TRIAGE)


def main():
    for i in range(0, 100):
        print("Time: ", GetServiceTriage())


main()