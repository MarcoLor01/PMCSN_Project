from controller.TriageController import *
from utility.ArrivalService import *
import logging
from controller.QueueController import *

# Configurazione del logger
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

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
        #pre_process_triage()
        t_triage.min_completion, t_triage.server_index = min_time_completion(
            t_triage.completion + [INFINITY])  # include INFINITY for queue check
        t_triage.next = minimum(t_triage.arrival, t_triage.min_completion)  # next event time

        if number_triage > 0:
            area_triage.node += (t_triage.next - t_triage.current) * number_triage
            area_triage.queue += (t_triage.next - t_triage.current) * (number_triage - sum(servers_busy_triage))
            for i in range(NUMERO_DI_SERVER_TRIAGE):
                area_triage.service[i] = area_triage.service[i] + (t_triage.next - t_triage.current) * \
                                         servers_busy_triage[i]

        t_triage.current = t_triage.next  # advance the clock

        if t_triage.current == t_triage.arrival:  # process an arrival
            number_triage += 1
            job = Job(arrivalTemp)
            job.triage(give_code())
            add_job_to_queue(job, queue_triage)
            arrivalTemp = arrivalTemp + GetArrival()
            t_triage.arrival = arrivalTemp

            if t_triage.arrival > STOP:
                t_triage.last = t_triage.current
                t_triage.arrival = INFINITY

            for i in range(NUMERO_DI_SERVER_TRIAGE):
                if not servers_busy_triage[i]:  # check if server is free
                    job_to_serve = get_next_job_to_serve(queue_triage)
                    if job_to_serve:
                        servers_busy_triage[i] = True
                        t_triage.completion[i] = t_triage.current + GetServiceTriage()
                        break

        else:  # process a completion
            index_triage += 1
            number_triage -= 1
            servers_busy_triage[t_triage.server_index] = False
            t_triage.completion[t_triage.server_index] = INFINITY
            area_triage.jobs_completed[t_triage.server_index] += 1

            job_to_serve = get_next_job_to_serve(queue_triage)

            if job_to_serve:
                servers_busy_triage[t_triage.server_index] = True
                t_triage.completion[t_triage.server_index] = t_triage.current + GetServiceTriage()
                area_triage.wait_time[
                    job_to_serve.get_codice() - 1] += t_triage.current - job_to_serve.get_arrival_temp()
                area_triage.jobs_complete_color[job_to_serve.get_codice() - 1] += 1
                pass_to_queue(job_to_serve)

    logger.info(f"Average interarrival time: {t_triage.last / sum(area_triage.jobs_completed):.2f}")
    logger.info(f"Average wait: {area_triage.node / sum(area_triage.jobs_completed):.2f}")
    logger.info(f"Average delay: {area_triage.queue / sum(area_triage.jobs_completed):.2f}")
    logger.info(f"Average service time: {sum(area_triage.service) / sum(area_triage.jobs_completed):.2f}")
    logger.info(f"Average number_triage in the node: {area_triage.node / t_triage.current:.2f}")
    logger.info(f"Average number_triage in the queue: {area_triage.queue / t_triage.current:.2f}")

    for i in range(NUMERO_DI_SERVER_TRIAGE):
        utilization = area_triage.service[i] / t_triage.current if t_triage.current > 0 else 0
        avg_service_time = area_triage.service[i] / area_triage.jobs_completed[i] if area_triage.jobs_completed[
                                                                                         i] > 0 else 0

        logger.info(f"Utilization of server {i + 1}: {utilization:.2f}")
        logger.info(f"Average service time of server {i + 1}: {avg_service_time:.2f}")
    for i in range(len(queue_triage)):
        if area_triage.jobs_complete_color[i] != 0:
            #logger.info(f"Waiting time for color {i + 1}: {area_triage.wait_time[i]}")
            #logger.info(f"job for color {i + 1}: {area_triage.jobs_complete_color[i]}")
            logger.info(f"Attesa media {i + 1}: {area_triage.wait_time[i] / area_triage.jobs_complete_color[i]}")


def main():
    simulation()


if __name__ == "__main__":
    main()
