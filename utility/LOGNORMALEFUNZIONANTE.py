# from utility.Parameters import *
# from utility.Rngs import selectStream, plantSeeds
# from utility.Rngs import DEFAULT
# from utility.Rvgs import Exponential, Lognormal
# from model.Job import Job
# import numpy as np
#
# summary = 0
# max_simulation = 2000000
# step_size = 500
# iteration = 0
# arrivalTemp = START  # global temp var for getArrival function
#
# plantSeeds(DEFAULT)
#
#
# def GetArrival():
#     # ---------------------------------------------
#     # * generate the next arrival time, with rate 1/2
#     # * ---------------------------------------------
#     # */
#     global arrivalTemp
#     selectStream(0)
#     arrivalTemp += Exponential(1 / TASSO_DI_INGRESSO)  # Lavoriamo su job al minuto
#     newJob = Job(int(arrivalTemp))
#     return newJob
#
#
# def GetServiceTriage(code):
#     # --------------------------------------------
#     # * generate the next service time with rate 1/2
#     # * --------------------------------------------
#     # */
#     selectStream(2)
#     mean=15
#     sigma=0.2
#     muu = np.log(mean**2 / np.sqrt(sigma**2 + mean**2))
#     sigmaa = np.sqrt(np.log(sigma**2 / mean**2 + 1))
#
#     mu = MU_VALORI[code]
#     sigma = SIGMA_VALORI[code]
#     media=4.997
#     var=-3.9
#     return Lognormal(muu, sigmaa)
#
# j=0
# max=0
# arr=5
# minimo=1000
# def main():
#     global j
#     global max
#     global arr
#     global minimo
#     for i in range(0, 1000000):
#         temp= GetServiceTriage(arr)
#         if temp>max:
#             max=temp
#
#         if temp<minimo:
#             minimo=temp
#         j= j+temp
#     print("Res:", j / 1000000)
#     print("Max:", max)
#     print("Minimo:", minimo)
#
#
# main()
#