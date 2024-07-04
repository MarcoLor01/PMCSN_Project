class Job:
    def __init__(self, istante_arrivo: int):
        self.__codice = None
        self.__istante_arrivo = istante_arrivo
        self.__istante_uscita = None
        self.__analisi_enum = None
        self.__interrotto = None
        self.__triage_time = None

    def initialize_job(self, istante_arrivo: int):
        self.__istante_arrivo = istante_arrivo

    def triage(self, codice: int):
        self.__codice = codice

    def set_time_triage(self, t: int):
        self.__triage_time = t

    def get_codice(self):
        return self.__codice

    def get_arrival_temp(self):
        return self.__istante_arrivo

    def get_time_triage(self):
        return self.__triage_time