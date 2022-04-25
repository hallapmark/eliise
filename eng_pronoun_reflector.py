from typing import List

class ENGPronounReflector:
    PRONOUN_REFLECTIONS = {
        "my": "your",
        "your": "my",
        "yours": "mine",
        "you": "me",
        "me": "you"
    }

    def reflect_pronouns(self, word_list: List[str]) -> List[str]:
        d = self.PRONOUN_REFLECTIONS
        return list(map(lambda word: d[word] if word in d else word, word_list))
