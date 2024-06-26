from typing import List
from utility.AnalisiEnum import Analisi
from utility.CodeEnum import Code


class Job:
    def __init__(self, istante_arrivo: int):
        self.__codice = None
        self.__istante_arrivo = istante_arrivo
        self.__istante_uscita = None
        self.__analisi_enum = None
        self.__interrotto = None

    def initializeJob(self, istante_arrivo: int):
        self.__istante_arrivo = istante_arrivo

    def triage(self, codice: Code):
        self.__codice = codice

    def getCodice(self):
        return self.__codice
