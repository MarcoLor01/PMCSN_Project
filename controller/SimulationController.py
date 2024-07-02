from controller.TriageController import *
from utility.ArrivalService import *
from controller.QueueController import *


summary = 0
max_simulation = 2000000
step_size = 500
iteration = 0
arrivalTemp = START  # global temp var for getArrival function

plantSeeds(DEFAULT)


def simulation():
    global arrivalTemp
    global number_triage, index_triage, queue_triage
    arrivalTemp = START
    arrivalTemp = arrivalTemp + GetArrival()

    init_triage(arrivalTemp)

    while (t_triage.arrival < STOP) or (number_triage > 0):
        pre_process_triage(t_triage, area_triage, number_triage, servers_busy_triage)

        if t_triage.current == t_triage.arrival:  # process an arrival
            number_triage += 1
            job = Job(arrivalTemp)
            job.triage(give_code())
            add_job_to_queue(job, queue_triage)
            arrivalTemp = arrivalTemp + GetArrival()
            t_triage.arrival = arrivalTemp
            arrival_triage(t_triage,servers_busy_triage, queue_triage)

        else:  # process a completion
            index_triage += 1
            number_triage -= 1
            job_to_serve = completition_triage(t_triage,servers_busy_triage, queue_triage, area_triage)
            if job_to_serve:
                pass_to_queue(job_to_serve)

    triage_data(area_triage,t_triage,queue_triage)

def main():
    simulation()


if __name__ == "__main__":
    main()
