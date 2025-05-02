class WoordAnalyse:
    def bepaal_lidwoord(self, woord: str) -> str:
        """Retourneert: 'de', 'het' of 'een'"""
        # TODO
        ...

    def is_verkleinwoord(self, woord: str) -> bool:
        """Retourneert: True als verkleinwoord"""
        # TODO
        ...

    def bepaal_woordsoort(self, woord: str) -> str:
        """Retourneert: woordsoort zoals 'zelfstandig naamwoord'"""
        # TODO
        ...

    def vervoeg_werkwoord(self, infinitief: str, tijd: str, persoon: str) -> str:
        """Retourneert: vervoegde werkwoordsvorm"""
        # TODO
        ...

    def maak_meervoud(self, zelfstandig_naamwoord: str) -> str:
        """Retourneert: meervoudsvorm"""
        # TODO
        ...

    def maak_verkleinwoord(self, zelfstandig_naamwoord: str) -> str:
        """Retourneert: verkleinwoord"""
        # TODO
        ...

    def is_samenstelling(self, woord: str) -> bool:
        """Retourneert: True als samenstelling"""
        # TODO
        ...

    def analyseer_woordbouw(self, woord: str) -> dict:
        """Retourneert: {'prefix': ..., 'stam': ..., 'suffix': ...}"""
        # TODO
        ...

    def detect_leenwoord(self, woord: str) -> bool:
        """Retourneert: True als leenwoord"""
        # TODO
        ...