from typing import List
from utility.AnalisiEnum import Analisi
from utility.CodeEnum import Code


class Job:
    def __init__(self, codice: Code, istante_arrivo: int, istante_uscita: int, analisi_enum: List[Analisi], interrotto: bool = False):
        self.codice = codice
        self.istante_arrivo = istante_arrivo
        self.istante_uscita = istante_uscita
        self.analisi_enum = analisi_enum
        self.interrotto = interrotto
