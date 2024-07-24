from utility.Utils import *
from utility.ArrivalService import *
from model.Job import *

queueRed_Radiografia = []
queueNotRed_Radiografia = []
queue_Radiografia = [queueRed_Radiografia, queueNotRed_Radiografia]

server_Radiografia = [Job] * NUMERO_DI_SERVER_RADIOGRAFIA
area_Radiografia = Track(NUMERO_DI_SERVER_RADIOGRAFIA, len(queue_Radiografia))
t_Radiografia = Time(NUMERO_DI_SERVER_RADIOGRAFIA)

index_Radiografia = 0
number_Radiografia = 0.0
servers_busy_Radiografia = [False] * NUMERO_DI_SERVER_RADIOGRAFIA  # track busy/free status of servers
