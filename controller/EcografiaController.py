from utility.Utils import *
from utility.ArrivalService import *
from model.Job import *

queueRed_Ecografia = []
queueNotRed_Ecografia = []
queue_Ecografia = [queueRed_Ecografia, queueNotRed_Ecografia]

server_Ecografia = [Job] * NUMERO_DI_SERVER_ECOGRAFIA
area_Ecografia = Track(NUMERO_DI_SERVER_ECOGRAFIA, len(queue_Ecografia))
t_Ecografia = Time(NUMERO_DI_SERVER_ECOGRAFIA)

index_Ecografia = 0
number_Ecografia = 0.0
servers_busy_Ecografia = [False] * NUMERO_DI_SERVER_ECOGRAFIA  # track busy/free status of servers
