tokens_to_find: list[str] = [
    "(",
    ")",
    "!",
    "\"",
    "\n"
]


class Tokeniser:
    def __init__(self, text: str):
        self.text: str = text

        self.found_tokens: list[str] = []

        self.buf: str = ""
        self.idx: int = 0
        self.program_len: int = len(text)

    def parse_string(self):
        # Find the other "
        self.idx += 1

        try:
            while self.text[self.idx] != "\"":
                self.buf += self.text[self.idx]
                self.idx += 1

            self.buf += self.text[self.idx]
        except IndexError:
            print("Error: No end of string found.")
            exit(1)

    def consume(self):
        if self.buf == "\"":
            self.parse_string()

        self.found_tokens.append(self.buf.strip())
        self.buf = ""

    def tokenise(self):
        # Go through the code and look to find all the tokens
        while self.idx < self.program_len:
            self.buf += self.text[self.idx]
            if self.idx == self.program_len - 1:
                self.consume()
            elif self.buf in tokens_to_find or self.text[self.idx + 1] in tokens_to_find:  # lang idea: xor
                self.consume()

            self.idx += 1

        while '' in self.found_tokens:
            self.found_tokens.pop(self.found_tokens.index(''))

        return self.found_tokens
