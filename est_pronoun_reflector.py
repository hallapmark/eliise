from typing import List

class ESTPronounReflector:
    PRONOUN_REFLECTIONS = {
        "mina": "sina",
        "ma": "sa",
        "sina": "mina",
        "sa": "ma",
        "minu": "sinu",
        "mu": "su",
        "sinu": "minu",
        "su": "mu",
        "mul": "sul",
        "sul": "mul",
        "mulle": "sulle",
        "sulle": "mulle",
        "mind": "sind",
        "sind": "mind"
    }

    def reflect_pronouns(self, word_list: List[str]) -> List[str]:
        d = self.PRONOUN_REFLECTIONS
        return [(d[word] if word in d else word) for word in word_list]
