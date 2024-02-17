class Tokeniser:
    def __init__(self, text:str):
        self.text:str = text

        self.found_tokens:list[str] = []
        self.tokens_to_find:list[str] = [
                "(",
                ")",
                "!",
                "\"",
                "\n"
                ]
        
        self.buf:str = ""
        self.idx:int = 0
        self.program_len:int = len(text)

    def consume(self):
        self.found_tokens.append(self.buf)
        self.buf = ""

    def tokenise(self):
        # Go through the code and look to find all the tokens
        while self.idx < self.program_len:
            self.buf += self.text[self.idx]
            if self.idx == self.program_len - 1:
                self.consume()
            elif self.buf in self.tokens_to_find or self.text[self.idx+1] in self.tokens_to_find:
                    self.consume()

            self.idx += 1

        return self.found_tokens