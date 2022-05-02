from estnltk import Text
from typing import List

class ESTTokenizer:
    words_key = 'words'

    def tokenized(self, message) -> List[str]:
        est_text = Text(message).tag_layer([self.words_key])
        return [word.text for word in est_text.words]

if __name__ == "__main__":
    tokenizer = ESTTokenizer()
    test = tokenizer.tokenized("Karu jooksis sookollide eest pakku.")
    print(test)
    