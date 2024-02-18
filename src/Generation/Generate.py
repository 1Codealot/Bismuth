from src.Tokenisation import Tokeniser


class CodeGenerator:
    def __init__(self, code):
        self.tokens = Tokeniser.Tokeniser(open(code, 'r').read()).tokenise()  # Best line of code ever written lol.

        self.builtin_functions = {
            "exit": self.write_exit,
            "print": self.write_print
        }

        self.data: list[str] = []  # For `section .data` in asm
        self.text: list[str] = []

        self.strings: int = 0

    def write_print(self, args: list[str]):
        if len(args) != 1:
            raise SyntaxError

        self.data.append(f"""
    s{self.strings} db {str(list(map(ord, args[0].strip('"').encode().decode('unicode_escape')))).strip("[]")}, 0
    s{self.strings}l equ $ - s{self.strings}""")

        self.text.append(
            f"""
    mov rax, 1
    mov rdi, 1
    mov rsi, s{self.strings}
    mov rdx, s{self.strings}l
    syscall""")
        self.strings += 1

    def write_exit(self, args: list[str]):
        if len(args) != 1:
            raise SyntaxError

        self.text.append(
            f"""
    mov rax, 60
    mov rdi, {args[0]}
    syscall""")

    def write_code(self):
        with open("./out/out.asm", 'w') as f:
            f.write("section .data")
            for sec in self.data:
                f.write(sec + "\n")

            f.write("\n\n")
            f.write("section .text\n")
            f.write("global _start\n")
            f.write("_start:")

            for sec in self.text:
                f.write(sec + "\n")

    def parse(self):
        token_idx: int = 0
        while token_idx < len(self.tokens):
            if (func_token := self.tokens[token_idx]) in self.builtin_functions:
                token_idx += 1
                if self.tokens[token_idx] != "(":
                    print("Error: Expected `(`")
                    exit(1)

                token_idx += 1
                args: list = []

                while self.tokens[token_idx] != ")":
                    args.append(self.tokens[token_idx])
                    token_idx += 1

                try:
                    self.builtin_functions[func_token](args)
                except SyntaxError:
                    print(f"Error: Args passed to `{func_token}` is not right.")
                    exit(1)
            else:
                if func_token not in Tokeniser.tokens_to_find:
                    print(f"Unknown function or key word `{func_token}`.")
                    exit(1)

            token_idx += 1
