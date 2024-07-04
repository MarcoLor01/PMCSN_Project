from utility.Rngs import random, selectStream
from utility.Utils import *
from utility.Parameters import *
from model.Job import *
from utility.ArrivalService import *

queueRed_Tac = []
queueNotRed_Tac = []
queue_Tac = [queueRed_Tac, queueNotRed_Tac]

server_Tac = [Job] * NUMERO_DI_SERVER_TAC
area_Tac = Track(NUMERO_DI_SERVER_TAC, len(queue_Tac))
t_Tac = Time(NUMERO_DI_SERVER_TAC)

index_Tac = 0
number_Tac = 0.0
servers_busy_Tac = [False] * NUMERO_DI_SERVER_TAC  # track busy/free status of servers
