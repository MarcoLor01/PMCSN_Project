from utility.Utils import *
from utility.ArrivalService import *
from model.Job import *

queueRed_Ecg = []
queueNotRed_Ecg = []
queue_Ecg = [queueRed_Ecg, queueNotRed_Ecg]

server_Ecg = [Job] * NUMERO_DI_SERVER_ECG
area_Ecg = Track(NUMERO_DI_SERVER_ECG, len(queue_Ecg))
t_Ecg = Time(NUMERO_DI_SERVER_ECG)

index_Ecg = 0
number_Ecg = 0.0
servers_busy_Ecg = [False] * NUMERO_DI_SERVER_ECG  # track busy/free status of servers
