from utility.Rngs import random, selectStream
from utility.Utils import *
from utility.Parameters import *
from model.Job import *
from utility.ArrivalService import *

queueRed_Emocromo = []
queueNotRed_Emocromo = []
queue_Emocromo = [queueRed_Emocromo, queueNotRed_Emocromo]

server_Emocromo = [Job] * NUMERO_DI_SERVER_EMOCROMO
area_Emocromo = Track(NUMERO_DI_SERVER_EMOCROMO, len(queue_Emocromo))
t_Emocromo = Time(NUMERO_DI_SERVER_EMOCROMO)

index_Emocromo = 0
number_Emocromo = 0.0
servers_busy_Emocromo = [False] * NUMERO_DI_SERVER_EMOCROMO  # track busy/free status of servers
