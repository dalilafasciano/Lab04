class LingottoFiere:
    def __init__(self, nome):
        """Inizializza gli attributi e le strutture dati"""
        self.nome = nome
        self.stand = []
        self.espositori = []

    """Aggiungere setter e getter se necessari"""

    def get_nome(self):
        return self.nome

    def set_nome(self, nome):
        self.nome = nome

    class Stand:
        def __init__(self, codice, superficie, padiglione, prezzo_base):
            self.codice = codice
            self.superficie = float(superficie)
            self.padiglione = int(padiglione)
            self.prezzo_base = float(prezzo_base)
            self.disponibile = True
            self.espositore = None

        @property
        def prezzo(self):
            return self.prezzo_base

        def __eq__(self, other):
            return isinstance(other, LingottoFiere.Stand) and self.codice == other.codice

        def __lt__(self, other):
            return self.prezzo < other.prezzo

        def __str__(self):
            stato = "Disponibile" if self.disponibile else "Non disponibile"
            return (f"{self.codice}: Standard | {self.superficie:g} mq - "
                    f"Padiglione {self.padiglione} - Prezzo {self.prezzo:.2f}€ - {stato}")

    class StandPreseExtra:
        def __init__(self, codice, superficie, padiglione, prezzo_base, prese_extra):
            self.codice = codice
            self.superficie = float(superficie)
            self.padiglione = int(padiglione)
            self.prezzo_base = float(prezzo_base)
            self.prese_extra = int(prese_extra)
            self.disponibile = True
            self.espositore = None

        def __eq__(self, other):
            return hasattr(other, "codice") and self.codice == other.codice

        def __lt__(self, other):
            return self.prezzo < other.prezzo

        @property
        def prezzo(self):
            return self.prezzo_base * (1 + 0.07 * self.prese_extra)

        def __str__(self):
            stato = "Disponibile" if self.disponibile else "Non disponibile"
            return (f"{self.codice}: Prese Extra | {self.superficie:g} mq - "
                    f"Padiglione {self.padiglione} - Prezzo {self.prezzo:.2f}€ - "
                    f"Prese aggiuntive: {self.prese_extra} - {stato}")

    class StandPremium:
        def __init__(self, codice, superficie, padiglione, prezzo_base, posizione):
            self.codice = codice
            self.superficie = float(superficie)
            self.padiglione = int(padiglione)
            self.prezzo_base = float(prezzo_base)
            self.posizione = posizione
            self.disponibile = True
            self.espositore = None

        def __eq__(self, other):
            return hasattr(other, "codice") and self.codice == other.codice

        def __lt__(self, other):
            return self.prezzo < other.prezzo

        @property
        def prezzo(self):
            return self.prezzo_base * 1.30

        def __str__(self):
            stato = "Disponibile" if self.disponibile else "Non disponibile"
            return (f"{self.codice}: Premium ({self.posizione}) | "
                    f"{self.superficie:g} mq - Padiglione {self.padiglione} - "
                    f"Prezzo {self.prezzo:.2f}€ - {stato}")

    class Espositore:
        def __init__(self, codice, nome, cognome):
            self.codice = codice
            self.nome = nome
            self.cognome = cognome
            self.stand = None

        def __eq__(self, other):
            return isinstance(other, LingottoFiere.Espositore) and self.codice == other.codice

        def __str__(self):
            descrizione = f"{self.codice}: {self.nome} {self.cognome}"
            if self.stand is not None:
                descrizione += f" - Stand assegnato: {self.stand.codice}"
            else:
                descrizione += " - Nessuno stand assegnato"
            return descrizione

    def carica_file_dati(self, file_path):
        self.stand = []
        self.espositori = []

        with open(file_path, "r", encoding="utf-8") as file:
            for riga in file:
                riga = riga.strip()

                if not riga:
                    continue

                dati = [campo.strip() for campo in riga.split(",")]
                codice = dati[0]

                if codice.startswith("ST"):
                    superficie = float(dati[1])
                    padiglione = int(dati[2])
                    prezzo_base = float(dati[3])

                    if len(dati) == 4:
                        stand = self.Stand(
                            codice, superficie, padiglione, prezzo_base
                        )
                    else:
                        try:
                            prese_extra = int(dati[4])
                            stand = self.StandPreseExtra(
                                codice, superficie, padiglione,
                                prezzo_base, prese_extra
                            )
                        except ValueError:
                            stand = self.StandPremium(
                                codice, superficie, padiglione,
                                prezzo_base, dati[4]
                            )

                    self.stand.append(stand)

                elif codice.startswith("ES"):
                    self.espositori.append(
                        self.Espositore(codice, dati[1], dati[2])
                    )


    def assegna_stand_a_espositore(self, codice_stand, codice_espositore):
        """Associa uno stand a un espositore"""
        stand = next(
            (s for s in self.stand if s.codice == codice_stand), None
        )

        espositore = next(
            (e for e in self.espositori
             if e.codice == codice_espositore), None
        )

        if stand is None:
            raise ValueError(f"Stand {codice_stand} inesistente")

        if espositore is None:
            raise ValueError(f"Espositore {codice_espositore} inesistente")

        if not stand.disponibile:
            raise ValueError(f"Stand {codice_stand} non disponibile")

        if espositore.stand is not None:
            raise ValueError(
                f"L'espositore {codice_espositore} ha già uno stand assegnato"
            )

        stand.disponibile = False
        stand.espositore = espositore
        espositore.stand = stand

    def elenca_espositori(self):
        """Stampa l'elenco degli espositori mostrando, per ognuno, lo stand a cui è associato, quando applicabile """
        for espositore in self.espositori:
            print(espositore)

    def stand_ordinati_per_prezzo(self):
        """Restituisce la lista ordinata degli stand in base al prezzo"""
        return sorted(self.stand, key=lambda stand: stand.prezzo)
