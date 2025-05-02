class ZinsAnalyse:
    def check_woordvolgorde(self, zin: str) -> bool:
        """Retourneert: True als correct"""
        # TODO
        ...

    def ontleed_zin(self, zin: str) -> list:
        """Retourneert: lijst van zinsdelen met functie"""
        # TODO
        ...

    def detect_zinstype(self, zin: str) -> str:
        """Retourneert: 'vraagzin', 'mededelende zin', of 'gebiedende zin'"""
        # TODO
        ...

    def detect_tijd(self, zin: str) -> str:
        """Retourneert: tijdsaanduiding"""
        # TODO
        ...

    def detect_inversie(self, zin: str) -> bool:
        """Retourneert: True als inversie"""
        # TODO
        ...

    def is_inversie_nodig(self, zin: str) -> bool:
        """Retourneert: True als inversie vereist"""
        # TODO
        ...

    def detect_dubbele_negatie(self, zin: str) -> tuple[bool, str]:
        """Retourneert: (True, uitleg) bij dubbele negatie"""
        # TODO
        ...

    def analyseer_zinsdelen(self, zin: str) -> list[tuple[str, str]]:
        """Retourneert: (zinsdeel, functie)"""
        # TODO
        ...

    def detect_congruentie_fouten(self, zin: str) -> list[str]:
        """Retourneert: lijst met fouten"""
        # TODO
        ...

    def detect_woordherhaling(self, zin: str) -> list[str]:
        """Retourneert: lijst van herhalingen"""
        # TODO
        ...

    def vereenvoudig_zin(self, zin: str) -> str:
        """Retourneert: vereenvoudigde zin"""
        # TODO
        ...
