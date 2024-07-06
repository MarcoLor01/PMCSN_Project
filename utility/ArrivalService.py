from utility.Parameters import *
from utility.Rngs import selectStream, plantSeeds
from utility.Rngs import DEFAULT
from utility.Rvgs import Exponential, Uniform
from model.Job import Job

#summary = 0
#max_simulation = 2000000
#step_size = 500
#iteration = 0
#arrivalTemp = START  # global temp var for getArrival function

#plantSeeds(DEFAULT)


def GetArrival():
    # ---------------------------------------------
    # * generate the next arrival time, with rate 1/2
    # * ---------------------------------------------
    # */
    selectStream(0)
    return Exponential(1 / TASSO_DI_INGRESSO)


def GetServiceTriage():
    # --------------------------------------------
    # * generate the next service time with rate 1/2
    # * --------------------------------------------
    # */
    selectStream(2)
    return Uniform(SX_SERVIZIO_TRIAGE, DX_SERVIZIO_TRIAGE)

def GetServiceQueue():
    # --------------------------------------------
    # * generate the next service time with rate 1/2
    # * --------------------------------------------
    # */
    selectStream(4)
    return Uniform(20, 40)


def GetServiceAnalisi(analisi):
    # --------------------------------------------
    # * generate the next service time with rate 1/2
    # * --------------------------------------------
    # */
    selectStream(10)
    return Uniform(2, 5)
#j=0
#max=0
#min=100

#USATA PER VEDERE CHE GENERIAMO I NUMERI GIUSTI
def testDistribution():
    global j
    global max
    global min
    for i in range(0, 1000000):
        temp= GetServiceTriage()
        if temp > max:
            max = temp
        if temp < min:
            min = temp
        j= j+temp
        print("Time: ",temp)
    print("Res:", j / 1000000)
    print("Max:", max)
    print("Min:", min)


