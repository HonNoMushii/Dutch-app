class SpellingEnStijl:
    def check_spelling(self, zin: str) -> list[str]:
        """Retourneert: lijst fout gespelde woorden"""
        # TODO
        ...

    def geef_verbetersuggesties(self, zin: str) -> list[tuple[str, str]]:
        """Retourneert: (fout, suggestie)"""
        # TODO
        ...

    def is_passieve_zin(self, zin: str) -> bool:
        """Retourneert: True als zin passief is"""
        # TODO
        ...

    def detect_tautologie(self, zin: str) -> list[str]:
        """Retourneert: gevonden tautologieën"""
        # TODO
        ...

    def detect_contaminatie(self, zin: str) -> list[str]:
        """Retourneert: contaminaties"""
        # TODO
        ...

    def check_formaliteit(self, zin: str) -> str:
        """Retourneert: 'formeel', 'informeel', 'neutraal'"""
        # TODO
        ...

    def detect_loze_woorden(self, zin: str) -> list[str]:
        """Retourneert: overbodige woorden"""
        # TODO
        ...
