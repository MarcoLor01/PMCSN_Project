from utility.Parameters import INFINITY
def minimum(a, c):
    # ------------------------------
    # * return the smaller of a, b
    # * ------------------------------
    # */
    if a < c:
        return a
    else:
        return c


def min_time_completion(completion_times):
    """Returns the minimum completion time and the index of the server"""
    #for i in range(len(completion_times)):
    #    print(i, completion_times[i])
    min_completion_time = min(completion_times)
    min_index = completion_times.index(min_completion_time)
    return min_completion_time, min_index


def get_next_job_to_serve(list_of_queues):
    """Selects the next job to serve based on a priority policy"""
    for queue in list_of_queues:
        if queue:
            return queue.pop(0)  # Simple FIFO (First In, First Out) policy for each priority queue
    return None


def add_job_to_queue(job, queue):
    index = job.get_codice() - 1  # Utilizza getCodice per determinare l'indice della lista
    if 0 <= index < len(queue):
        queue[index].append(job)
    else:
        print(f"Index {index} is out of range for list_of_queues")


class Track:
    def __init__(self, num_serv, num_queue):
        self.node = 0.0  # time integrated number in the node
        self.queue = 0.0  # time integrated number in the queue
        self.service = [0.0] * num_serv  # time integrated number in service
        self.jobs_completed = [0] * num_serv
        self.wait_time = [0.0] * num_queue
        self.jobs_complete_color = [0] * num_queue


class Time:
    def __init__(self, num_serv):
        self.arrival = -1  # next arrival time
        self.completion = [INFINITY] * num_serv  # next completion times for each server
        self.min_completion = INFINITY
        self.server_index = -1
        self.current = -1  # current time
        self.next = -1  # next (most imminent) event time
        self.last = -1  # last arrival time
