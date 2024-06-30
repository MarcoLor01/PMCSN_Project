from utility.ArrivalService import *
from utility.Utils import Minimum

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


def Simulation():

    global arrivalTemp
    index = 0  # used to count departed jobs         */
    number = 0  # number in the node                  */
    arrivalTemp = arrivalTemp + GetArrival()
    t.arrival = arrivalTemp  # schedule the first arrival            */
    while (t.arrival < STOP) or (number > 0):
        t.next = Minimum(t.arrival, t.completion)  # next event time   */
        if number > 0:  # update integrals  */
            area.node += (t.next - t.current) * number
            area.queue += (t.next - t.current) * (number - 1)
            area.service += (t.next - t.current)
        # EndIf

        t.current = t.next  # advance the clock */

        if t.current == t.arrival:  # process an arrival */

            number += 1
            arrivalTemp = arrivalTemp + GetArrival()
            t.arrival = arrivalTemp

            if t.arrival > STOP:
                t.last = t.current
                t.arrival = INFINITY
            if number == 1:
                t.completion = t.current + GetServiceTriage()

        # EndOuterIf
        else:  # process a completion */
            index += 1
            number -= 1

            if number > 0:
                t.completion = t.current + GetServiceTriage()
            else:
                t.completion = INFINITY

            # EndWhile
    print("   average interarrival time = {0:6.2f}".format(t.last / (index)))
    print("   average wait ............ = {0:6.2f}".format(area.node / (index)))
    print("   average delay ........... = {0:6.2f}".format(area.queue / (index)))
    print("   average service time .... = {0:6.2f}".format(area.service / (index)))
    print("   average # in the node ... = {0:6.2f}".format(area.node / t.current))
    print("   average # in the queue .. = {0:6.2f}".format(area.queue / t.current))
    print("   utilization ............. = {0:6.2f}".format(area.service / t.current))


area = track()
t = time()


def main():
    Simulation()


if __name__ == "__main__":
    main()
