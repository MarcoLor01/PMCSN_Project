from utility.CodeEnum import Code
from utility.Parameters import *
from utility.Rngs import selectStream, plantSeeds
from utility.Rngs import DEFAULT
from utility.Rvgs import Exponential, Lognormal
from model.Job import Job

summary = 0
max_simulation = 2000000
step_size = 500
iteration = 0
arrivalTemp = START  # global temp var for getArrival function

plantSeeds(DEFAULT)


def GetArrival():
    # ---------------------------------------------
    # * generate the next arrival time, with rate 1/2
    # * ---------------------------------------------
    # */
    global arrivalTemp
    selectStream(0)
    arrivalTemp += Exponential(1 / TASSO_DI_INGRESSO)  # Lavoriamo su job al minuto
    newJob = Job(int(arrivalTemp))
    return newJob


def GetServiceTriage(code: Code):
    # --------------------------------------------
    # * generate the next service time with rate 1/2
    # * --------------------------------------------
    # */
    selectStream(2)
    mu = MU_VALORI[code.name]
    sigma = SIGMA_VALORI[code.name]
    return Lognormal(mu, sigma)

j=0
max=0
arr=Code.BIANCO
def main():
    global j
    global max
    global arr
    for i in range(0, 1000000):
        temp= GetServiceTriage(arr)
        if temp>max:
            max=temp
        j= j+temp
        #print("Time: ",temp)
    print("Res:", j / 1000000)
    print("Max:", max)


main()
