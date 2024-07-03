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

    init_triage(arrivalTemp)
    init_queue(t_queue)
    while (t_triage.arrival < STOP) or (number_triage > 0) or (number_queue > 0):
        pre_process_triage(t_triage, area_triage, number_triage, servers_busy_triage)
        pre_process_queue(t_queue, area_queue, number_queue, servers_busy_queue)

        if t_triage.current == t_triage.arrival:  # process an arrival
            number_triage += 1
            job = Job(arrivalTemp)
            job.triage(give_code())
            add_job_to_queue(job, queue_triage)
            arrivalTemp = arrivalTemp + GetArrival()
            t_triage.arrival = arrivalTemp
            arrival_triage(t_triage, servers_busy_triage, queue_triage)

        if t_triage.current == t_triage.min_completion:  # process a completion
            index_triage += 1
            number_triage -= 1
            job_to_serve = completition_triage(t_triage, servers_busy_triage, queue_triage, area_triage)

            if job_to_serve:
                pass_to_queue(job_to_serve, queue)

        if t_queue.current == t_queue.min_completion:
                number_queue += 1
                t_queue.current = t_triage.current+1
                t_queue.arrival = t_triage.current+1
                arrival_queue(t_queue, servers_busy_queue, queue)
                #print(job_to_serve.get_arrival_temp())

                t_queue.min_completion, t_queue.server_index = min_time_completion(
                    t_queue.completion + [INFINITY])  # include INFINITY for queue check
                print(t_queue.min_completion, t_queue.server_index)
                t_queue.next = t_queue.min_completion  # next event time

        if t_queue.current >= t_queue.next:  # process a completion
            index_queue += 1
            number_queue -= 1
            #job_to_serves = completition_queue(t_queue, servers_busy_queue, queue, area_queue)
            servers_busy_queue[t_queue.server_index-1] = False
            t_queue.completion[t_queue.server_index-1] = INFINITY + 1
            area_queue.jobs_completed[t_queue.server_index-1] += 1
            t_queue.min_completion = None
            job_to_serve = get_next_job_to_serve(queue)

            if job_to_serve:
                servers_busy_queue[t_queue.server_index] = True
                t_queue.completion[t_queue.server_index] = t_queue.current + GetServiceQueue()
                area_queue.wait_time[
                    job_to_serve.get_codice() - 1] += t_queue.current - job_to_serve.get_arrival_temp()
                area_queue.jobs_complete_color[job_to_serve.get_codice() - 1] += 1
                print("il valore c'è")
                pass_to_analisi()


    triage_data(area_triage,t_triage,queue_triage)
    printtanalisi()

def main():
    simulation()


if __name__ == "__main__":
    main()
