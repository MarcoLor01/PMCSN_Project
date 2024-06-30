from utility.Utils import *
from utility.Parameters import *
from model.Job import *

queueRed = []
queueOrange = []
queueBlue = []
queueGreen = []
queueWhite = []
queueReturnRed = []
queueReturnNotRed = []
# queue for jobs waiting to be served divided for colors
queue = [queueRed, queueReturnRed, queueReturnNotRed, queueOrange, queueBlue, queueGreen, queueWhite]
area_queue = Track(NUMERO_DI_SERVER_QUEUE, len(queue))
t_triage = Time(NUMERO_DI_SERVER_QUEUE)
index_queue = 0
number_queue = 0


def pass_to_queue(job: Job):
    if job.get_codice() == 1:
        queue[job.get_codice() - 1].append(job)
    else:
        queue[job.get_codice() + 1].append(job)


def printt():
    for i in queue:
        print("Lunghezza coda: ", len(i))