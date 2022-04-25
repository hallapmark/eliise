from typing import List

class ENGTokenizer:
    def tokenized(self, message) -> List[str]:
        return message.split(" ")

if __name__ == "__main__":
    tokenizer = ENGTokenizer()
    test = tokenizer.tokenized("The bear ran from the swamp monsters")
    print(test)