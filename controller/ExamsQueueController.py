from utility.Utils import *
from utility.Parameters import *
from model.Job import *
from utility.ArrivalService import *


index_queueaaa = 0


def pass_to_analisi():
    index_queueaaa = index_queueaaa+1


def printtanalisi():
    print("Lunghezza coda: ", index_queueaaa)