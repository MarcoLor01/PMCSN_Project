class Job:
    def __init__(self, istante_arrivo: int):
        self.__codice = None
        self.__istante_arrivo = istante_arrivo
        self.__istante_uscita = None
        self.__analisi_enum = None
        self.__interrotto = None
        self.__triage_time = None
        self.__lista_analisi = None
        self.__queue_time = None
        self.__uscita = False

    def get_uscita(self):
        return self.__uscita

    def set_uscita(self, uscita: bool):
        self.__uscita = uscita

    def set_queue_time(self, queue_time: int):
        self.__queue_time = queue_time

    def get_queue_time(self):
        return self.__queue_time

    def set_lista_analisi(self, lista_analisi):
        if not isinstance(lista_analisi, list):
            self.__lista_analisi = [lista_analisi]
        else:
            self.__lista_analisi = lista_analisi

    def get_lista_analisi(self):
        return self.__lista_analisi

    def triage(self, codice: int):
        self.__codice = codice

    def set_time_triage(self, t: int):
        self.__triage_time = t

    def set_arrival_temp(self, t: int):
        self.__istante_arrivo = t

    def get_codice(self):
        return self.__codice

    def get_arrival_temp(self):
        return self.__istante_arrivo

    def get_time_triage(self):
        return self.__triage_time
