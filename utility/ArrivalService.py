import numpy as np
from utility.Parameters import *
from utility.Rngs import selectStream, plantSeeds
from utility.Rngs import DEFAULT
from utility.Rvgs import Exponential, Uniform, Lognormal
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
    return Exponential(MEDIA_SERVIZIO_TRIAGE)

def GetServiceQueue():
    # --------------------------------------------
    # * generate the next service time with rate 1/2
    # * --------------------------------------------
    # */
    selectStream(4)
    return Exponential(MEDIA_TASSO_DI_SERVIZIO_QUEUE)


def GetServiceAnalisi(analisi, media):
    # --------------------------------------------
    # * generate the next service time with rate 1/2
    # * --------------------------------------------
    # */
    selectStream(analisi+100)
    sigma = 2
    mu = np.log(media**2 / np.sqrt(sigma**2 + media**2))
    sigma = np.sqrt(np.log(sigma**2 / media**2 + 1))
    #print("media: ", media, "mu", mu, "sigma", sigma)
    #print (np.random.lognormal(mu, sigma),  Lognormal(mu, sigma))
#    return Uniform(10, 20)
    return Lognormal(mu, sigma)


#USATA PER VEDERE CHE GENERIAMO I NUMERI GIUSTI
def testDistribution():
    j=0
    max=0
    min=100
    maxsim=100000
    mediana=[]
    sotto_dieci = []
    sopra_venti = []
    for i in range(0, maxsim):
        temp = GetServiceAnalisi(0, 15)
        #print("Valore generato: ", temp)
        mediana.append(temp)
        if temp > max:
            max = temp
        if temp < min:
            min = temp
        if temp < 15:
            sotto_dieci.append(temp)
        if temp > 15:
            sopra_venti.append(temp)

        j= j+temp
        #print("Time: ",temp)

    print("Res:", j / maxsim)
    print("Max:", max)
    print("Min:", min)
    print("Val sotto il dieci: ", len(sotto_dieci))
    print("Val sopra il 20: ", len(sopra_venti))
    mediana.sort()

    print("Mediana: ", mediana[int(maxsim/2)])

#testDistribution()
# Ecg 5 min
# Ecografia 15 min NO PREEMPTION
# Emocromo 1.15 h NO PREEMPTION
# Tac 30 min NO PREEMPTION
# Radiografia 25 min NO PREEMPTION
# Altri Esami 35 minuti