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
        "mind": "sind",
        "sind": "mind",
        "minusse": "sinusse",
        "sinusse": "minusse",
        "minus": "sinus",
        "sinus": "minus",
        "minust": "sinust",
        "sinust": "minust",
        "mulle": "sulle",
        "sulle": "mulle",
        "minul": "sinul",
        "mul": "sul",
        "sinul": "minul",
        "sul": "mul",
        "minult": "sinult",
        "mult": "sult",
        "sinult": "minult",
        "sult": "mult",
        "minuks": "sinuks",
        "sinuks": "minuks",
        "minuga": "sinuga",
        "sinuga": "minuga",
        "minuna": "sinuna",
        "minuta": "sinuta",
        "sinuta": "minuta",
        "minuga": "sinuga",
        "sinuga": "minuga"
    }

    def reflect_pronouns(self, word_list: List[str]) -> List[str]:
        d = self.PRONOUN_REFLECTIONS
        word_list = [word.lower() for word in word_list]
        return [(d[word] if word in d else word) for word in word_list]
