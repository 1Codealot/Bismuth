tokens_to_find: list[str] = [
    # Symbols
    "(",
    ")",
    "!",
    "\"",
    "\n",
    ":",
    "=",
    # Keywords
    "var",
    "int"
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

    def parse_num(self):
        while self.text[self.idx + 1].isdigit():
            self.idx += 1
            self.buf += self.text[self.idx]

    def consume(self):
        if self.buf == "\"":
            self.parse_string()
        elif self.buf.isdigit():
            self.parse_num()

        self.found_tokens.append(self.buf.strip())
        self.buf = ""

    def tokenise(self):
        # Go through the code and look to find all the tokens
        while self.idx < self.program_len:
            self.buf += self.text[self.idx]
            if self.buf.isspace():
                self.buf = ""

            if self.idx == self.program_len - 1:
                self.consume()
            elif (self.buf in tokens_to_find) or (self.text[self.idx + 1] in tokens_to_find) or (self.buf.isdigit()):
                self.consume()

            self.idx += 1

        # Remove unnecessary 'tokens'
        # Empty tokens
        while '' in self.found_tokens:
            self.found_tokens.pop(self.found_tokens.index(''))

        # Comments
        for t in self.found_tokens:
            # TODO: Fix this.
            if t[0] == "`" and t[-1] == "`":
                self.found_tokens.pop(self.found_tokens.index(t))

        return self.found_tokens
