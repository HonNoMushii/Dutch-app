import re
import pickle
import random
from pathlib import Path
from collections import defaultdict
from typing import Optional, List, Dict


def is_valid_roman_numeral(s: str) -> bool:
    """Check of een string een geldige Romeinse cijfernotatie is."""
    return bool(re.fullmatch(r"M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})", s))


def roman_to_int(s: str) -> Optional[int]:
    """Converteer Romeins cijfer naar een geheel getal."""
    roman_map = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    if not is_valid_roman_numeral(s):
        return None
    total = 0
    prev_value = 0
    for c in reversed(s):
        value = roman_map[c]
        if value < prev_value:
            total -= value
        else:
            total += value
        prev_value = value
    return total


class WordEntry:
    """
    Een enkel woord met bijbehorende grammaticale informatie (POS, kenmerken, bron).
    """
    def __init__(self, word: str, pos: str, features: Optional[Dict[str, str]] = None, source: Optional[str] = None):
        self.word = word
        self.pos = pos
        self.features = features or {}
        self.source = source

    def __repr__(self):
        return f"<{self.pos}: {self.word} {self.features}>"

    def __str__(self):
        source_str = f" (bron: {self.source})" if self.source else ""
        return f"{self.word} [{self.pos}] {self.features}{source_str}"


class WordDatabase:
    """
    Klasse die woorden en grammaticale informatie inlaadt, organiseert en analyseert.
    """
    def __init__(self, debug: bool = False):
        self.words = defaultdict(list)
        self.by_pos = defaultdict(list)
        self.file_index = defaultdict(list)
        self.debug = debug

        self.heuristics = {
            r"werkwoord": "verb",
            r"vervoeging": "verb",
            r"infinitief": "verb",
            r"noun": "noun",
            r"zelfstandigenaamwoord": "noun",
            r"bijvoeglijk": "adj",
            r"adjectief": "adj",
            r"bijwoord": "adv",
            r"voornaamwoord": "pronoun",
            r"voorzetsel": "prep",
            r"voegwoord": "conj",
            r"lidwoord": "det",
            r"telwoord": "num",
            r"tussenwerpsel": "interj",
            r"hulpwerkwoord": "aux",
            r"partikel": "part",
            r"romeins": "num"
        }

        self.fixed_pos = {
            "ik": "pronoun", "jij": "pronoun",
            "de": "det", "en": "conj", "maar": "conj",
            "niemand": "pronoun", "elkaar": "pronoun",
            "zal": "aux"
        }

        self.form_features = {
            "infinitief": {"vorm": "infinitief"},
            "stam": {"vorm": "stam"},
            "ikvorm": {"persoon": "1", "getal": "ev"},
            "jijvorm": {"persoon": "2", "getal": "ev"},
            "hijvorm": {"persoon": "3", "getal": "ev"},
            "voltooid": {"vorm": "vd"},
            "verleden": {"tijd": "vt"},
            "tegenwoordig": {"tijd": "tt"},
            "mv": {"getal": "mv"},
            "ev": {"getal": "ev"},
            "dewoorden": {"geslacht": "de"},
            "hetwoorden": {"geslacht": "het"},
            "romeins": {"vorm": "romeins"}
        }

        self.irregular_stems = {
            "zijn": "ben", "hebben": "heb", "kunnen": "kan",
            "moeten": "moet", "willen": "wil", "mogen": "mag",
            "gaan": "ga", "komen": "kom", "eten": "eet",
            "geven": "geef", "zien": "zie", "zeggen": "zeg",
        }

    def infer_pos_from_path(self, path: str) -> Optional[str]:
        path = path.lower().replace("_", "-")
        for pattern, pos in self.heuristics.items():
            if re.search(pattern, path):
                return pos
        return None

    def _infer_features_from_path(self, path: str) -> Dict[str, str]:
        path = path.lower().replace("_", "-")
        inferred = {}
        for key, feats in self.form_features.items():
            if key in path:
                inferred.update(feats)
        return inferred

    def _infer_features_from_word(self, word: str) -> Dict[str, str]:
        features = {}
        if word.endswith("de") or word.endswith("den"):
            features["tijd"] = "vt"
        elif word.endswith("t"):
            features["tijd"] = "tt"
        if word.endswith("d") or word.endswith("t"):
            features["vorm"] = "stam"
        if is_valid_roman_numeral(word):
            features["vorm"] = "romeins"
        return features

    def add_word(self, word: str, pos: str, features: Optional[Dict[str, str]] = None, source: Optional[str] = None, line_number: Optional[int] = None):
        entry = WordEntry(word=word, pos=pos, features=features or {}, source=source)
        self.words[word].append(entry)
        self.by_pos[pos].append(entry)
        if source and line_number is not None:
            self.file_index[source].append((line_number, word))

    def load_data_folder(self, folder: str = "data"):
        print(f"\U0001F4C2 Data inladen uit: {folder}")
        for file in Path(folder).rglob("*.txt"):
            inferred_pos = self.infer_pos_from_path(file.name)
            if not inferred_pos and self.debug:
                print(f"⚠️  Bestand overgeslagen (geen herkenbare POS): {file}")
            self._load_plain_wordlist(file, inferred_pos, file.name)

    def _load_plain_wordlist(self, path: Path, default_pos: Optional[str], source: str):
        with path.open(encoding="utf-8") as f:
            for i, word in enumerate((line.strip() for line in f), start=1):
                if not word:
                    continue
                pos = self.fixed_pos.get(word) or default_pos
                features = self._infer_features_from_path(path.name)
                word_feats = self._infer_features_from_word(word)
                features.update(word_feats)
                if pos:
                    self.add_word(word, pos, features, source, line_number=i)

    def get_entries(self, word: str, pos: Optional[str] = None) -> List[WordEntry]:
        return [e for e in self.words.get(word, []) if not pos or e.pos == pos]

    def get_by_pos(self, pos: str) -> List[WordEntry]:
        return self.by_pos[pos]

    def find_stem(self, infinitive: str) -> Optional[str]:
        if infinitive in self.irregular_stems:
            return self.irregular_stems[infinitive]

        entries = self.get_entries(infinitive, pos="verb")
        if not any(e.features.get("vorm") == "infinitief" for e in entries):
            return None

        if infinitive.endswith("iëren"):
            return infinitive[:-5] + "eer"
        elif infinitive.endswith("eren"):
            return infinitive[:-2]
        elif infinitive.endswith("ën"):
            return infinitive[:-2]
        elif infinitive.endswith("en"):
            return infinitive[:-2]

        return None

    def get_conjugation_table(self, verb: str) -> Dict[str, List[WordEntry]]:
        entries = self.get_entries(verb, pos="verb")
        table = defaultdict(list)
        for entry in entries:
            key = entry.features.get("vorm") or entry.features.get("tijd") or "anders"
            table[key].append(entry)
        return dict(table)

    def print_all_pos_tags(self):
        print("\n\U0001F9E9 Unieke POS-tags:", sorted(self.by_pos))

    def print_random_examples(self):
        print("\n\U0001F50E Voorbeeldwoorden uit alle bestanden:")
        for source, lines in self.file_index.items():
            if lines:
                line_num, word = random.choice(lines)
                entries = self.get_entries(word)
                print(f"\n✅ '{word}' uit bestand '{source}' (regel {line_num}):")
                for e in entries:
                    print("→", e)
                for e in entries:
                    if e.pos == "verb":
                        stam = self.find_stem(e.word)
                        if stam:
                            print(f"🔹 Stam van '{e.word}': '{stam}'")
                        table = self.get_conjugation_table(e.word)
                        if table:
                            print(f"📋 Vervoegingen voor '{e.word}':")
                            for vorm, lst in table.items():
                                print(f"  - {vorm:<12}: {[v.word for v in lst]}")
                    elif e.pos == "num" and e.features.get("vorm") == "romeins":
                        getal = roman_to_int(e.word)
                        if getal is not None:
                            print(f"🔢 Romeins '{e.word}' → {getal}")

    def save_to_pickle(self, path: str = "words.pkl"):
        with open(path, "wb") as f:
            pickle.dump((self.words, self.by_pos), f)

    def load_from_pickle(self, path: str = "words.pkl"):
        with open(path, "rb") as f:
            self.words, self.by_pos = pickle.load(f)


if __name__ == "__main__":
    db = WordDatabase(debug=False)
    db.load_data_folder("data")

    print("\n🔍 POS-tags en woordstatistiek:")
    db.print_all_pos_tags()
    print(f"\n📊 Totaal unieke woorden: {len(db.words)}")
    for pos in sorted(db.by_pos):
        print(f"📊 {pos:<10}: {len(db.by_pos[pos])} woorden")

    db.print_random_examples()
