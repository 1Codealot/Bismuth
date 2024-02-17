from src.Tokenisation import Tokeniser
import os


class CodeGenerator:
    def __init__(self, code):
        self.tokens = Tokeniser.Tokeniser(open(code, 'r').read()).tokenise()  # Best line of code ever written lol.

        print(self.tokens)

        self.data: list[str] = []  # For `section .data` in asm
        self.text: list[str] = []

        self.strings: int = 0

    def write_print(self, string: str):
        self.data.append(f"""
    s{self.strings} db '{string}', 0
    s{self.strings}l equ $ - s{self.strings}""")

        self.text.append(
            f"""
    mov rax, 1
    mov rdi, 1
    mov rsi, s{self.strings}
    mov rdx, s{self.strings}l
    syscall""")
        self.strings += 1

    def write_exit(self, code: int):
        self.text.append(
            f"""
    mov rax, 60
    mov rdi, {code}
    syscall""")

    def write_code(self):
        try:
            os.mkdir("../../out/")
        except FileExistsError:
            pass

        with open("../../out/out.asm", 'w') as f:
            f.write("section .data")
            for sec in self.data:
                f.write(sec + "\n")

            f.write("\n\n")
            f.write("section .text\n")
            f.write("global _start\n")
            f.write("_start:")

            for sec in self.text:
                f.write(sec + "\n")


if __name__ == '__main__':
    cg = CodeGenerator("../../tests/print.px")
    cg.write_print("Hello ")
    cg.write_print("World!")
    cg.write_exit(0)
    cg.write_code()
