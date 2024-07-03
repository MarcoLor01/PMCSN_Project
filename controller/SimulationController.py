from controller.TriageController import *
from utility.ArrivalService import *
from controller.QueueController import *
from controller.ExamsQueueController import *

summary = 0
max_simulation = 2000000
step_size = 500
iteration = 0
arrivalTemp = START  # global temp var for getArrival function

plantSeeds(DEFAULT)


def simulation():

    global arrivalTemp
    global number_triage, number_queue, index_triage, index_queue, queue_triage, queue
    arrivalTemp = START
    arrivalTemp = arrivalTemp + GetArrival()
    contAnalisi = 0
    init_triage(arrivalTemp)
    init_queue()
    while (t_triage.arrival < STOP) or (number_triage > 0) or (number_queue > 0):
        pre_process_triage(t_triage, area_triage, number_triage, servers_busy_triage)
        pre_process_queue(area_queue, number_queue, servers_busy_queue)

        if t_triage.current == t_triage.arrival:  # process an arrival
            number_triage += 1
            job = Job(arrivalTemp)
            job.triage(give_code())
            add_job_to_queue(job, queue_triage)
            arrivalTemp = arrivalTemp + GetArrival()
            t_triage.arrival = arrivalTemp
            arrival_triage(t_triage, servers_busy_triage, queue_triage)

        elif t_triage.current == t_triage.min_completion:  # process a completion for triage
            index_triage += 1
            number_triage -= 1
            job_completed = completion_triage(t_triage, servers_busy_triage, queue_triage, area_triage)
            #number_queue += 1 #----> PROBLEMA QUI, SE AGGIORNO NON FINISCE MAI
            pass_to_queue(job_completed, queue, t_triage)


        if t_queue.current == t_queue.min_completion:  # process a completion
            index_queue += 1
            number_queue -= 1
            print(number_queue)
            job_to_analisi = completion_queue(t_queue, servers_busy_queue, queue, area_queue)
            contAnalisi = pass_to_analisi()

    triage_data(area_triage, t_triage, queue_triage)
    #printtanalisi()
    print("Analisi:", contAnalisi)
    print("Triage:  ", index_triage)
    print("Queue:  ", index_queue)


def main():
    simulation()


if __name__ == "__main__":
    main()
