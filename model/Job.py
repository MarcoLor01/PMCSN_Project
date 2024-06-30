class Job:
    def __init__(self, istante_arrivo: int):
        self.__codice = None
        self.__istante_arrivo = istante_arrivo
        self.__istante_uscita = None
        self.__analisi_enum = None
        self.__interrotto = None

    def initializeJob(self, istante_arrivo: int):
        self.__istante_arrivo = istante_arrivo

    def triage(self, codice: int):
        self.__codice = codice

    def getCodice(self):
        return self.__codice

    def getArrivalTemp(self):
        return self.__istante_arrivo
