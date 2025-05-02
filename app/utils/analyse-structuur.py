class StructuurAnalyse:
    def analyseer_zinlengte(self, tekst: str) -> float:
        """Retourneert: gemiddelde zinlengte"""
        # TODO
        ...

    def bepaal_tekststructuur(self, tekst: str) -> dict:
        """Retourneert: {'inleiding': ..., 'kern': ..., 'slot': ...}"""
        # TODO
        ...

    def detect_paragraafstructuur(self, tekst: str) -> list[str]:
        """Retourneert: lijst van paragraaffuncties"""
        # TODO
        ...

    def check_overgangen_tussen_zinnen(self, tekst: str) -> list[str]:
        """Retourneert: zinnen met zwakke overgangen"""
        # TODO
        ...
