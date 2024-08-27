from utility.Parameters import *
from utility.Rngs import selectStream, random
from utility.Rvgs import Exponential, Lognormal
from utility.rvms import idfTruncatedNormal
from utility import Parameters

def GetArrival():
    # ---------------------------------------------
    # * generate the next arrival time, with rate 1/2
    # * ---------------------------------------------
    # */
    selectStream(0)
    return Exponential(1 / Parameters.TASSO_DI_INGRESSO)


def GetServiceTriage():
    # --------------------------------------------
    # * generate the next service time with rate 1/2
    # * --------------------------------------------
    # */
    selectStream(2)
    if MODALITY:
        return Exponential(MEDIA_SERVIZIO_TRIAGE)
    else:
        return idfTruncatedNormal(MEDIA_SERVIZIO_TRIAGE, DEVIAZIONE_STANDARD_TRIAGE, LOWER_BOUND_TRIAGE, UPPER_BOUND_TRIAGE)


def GetServiceQueue():
    # --------------------------------------------
    # * generate the next service time with rate 1/2
    # * --------------------------------------------
    # */
    selectStream(4)
    if MODALITY:
        return Exponential(MEDIA_TASSO_DI_SERVIZIO_QUEUE)
    else:
        return idfTruncatedNormal(MEDIA_TASSO_DI_SERVIZIO_QUEUE, DEVIAZIONE_STANDARD_QUEUE, LOWER_BOUND_QUEUE, UPPER_BOUND_QUEUE)


def GetServiceAnalisi(analisi, media):
    # --------------------------------------------
    # * generate the next service time with rate 1/2
    # * --------------------------------------------
    # */
    selectStream(analisi + 8)
    if MODALITY:
        return Exponential(media)
    else:
        return idfTruncatedNormal(media, DEVIAZIONE_STANDARD_ANALISI[analisi], LOWER_BOUND_ANALISI[analisi], UPPER_BOUND_ANALISI[analisi])
