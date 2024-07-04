from utility.Rngs import random, selectStream
from utility.Utils import *
from utility.Parameters import *
from model.Job import *
from utility.ArrivalService import *

queueRed_AltriEsami = []
queueNotRed_AltriEsami = []
queue_altriEsami = [queueRed_AltriEsami, queueNotRed_AltriEsami]

server_altriEsami = [Job] * NUMERO_DI_SERVER_ALTRI_ESAMI
area_altriEsami = Track(NUMERO_DI_SERVER_ALTRI_ESAMI, len(queue_altriEsami))
t_altriEsami = Time(NUMERO_DI_SERVER_ALTRI_ESAMI)

index_altriEsami = 0
number_altriEsami = 0.0
servers_busy_altriEsami = [False] * NUMERO_DI_SERVER_ALTRI_ESAMI  # track busy/free status of servers
