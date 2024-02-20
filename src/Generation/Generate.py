from src.Tokenisation import Tokeniser


class Variable:
    def __init__(self, ident: str, type_of: str, val: str):
        self.ident = ident
        self.type_of = type_of
        self.val = val


class CodeGenerator:
    def __init__(self, code):
        self.tokens = Tokeniser.Tokeniser(open(code, 'r').read()).tokenise()  # Best line of code ever written lol.

        # print(f"Token = {self.tokens}")

        self.builtin_functions = {
            "exit": self.write_exit,
            "print": self.write_print
        }

        self.token_idx: int = 0

        self.vars: list[Variable] = []

        self.data: list[str] = []  # For `section .data` in asm
        self.text: list[str] = []

        self.strings: int = 0

    def get_var_names(self) -> list:
        return list(map(lambda v: v.ident, self.vars))

    def get_var_from_ident(self, ident: str) -> Variable:
        if ident not in self.get_var_names():
            raise NameError
        else:
            for v in self.vars:
                if v.ident == ident:
                    return v

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

        value = 0

        if args[0] in self.get_var_names():
            var = self.get_var_from_ident(args[0])  # No need to catch error because we check right above

            if var.type_of != "int":
                print(f"Type of variable {var.ident} not `int`")
            else:
                value = int(var.val)
        else:
            try:
                value = int(args[0])
            except ValueError:
                print("Error: Something went wrong.")
                exit(1)

        self.text.append(
            f"""
    mov rax, 60
    mov rdi, {value}
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

    def parse_var(self):
        if self.tokens[self.token_idx] == "var":
            self.token_idx += 2
            var_type = self.tokens[self.token_idx]

            self.token_idx += 1
            name = self.tokens[self.token_idx]
            if not name.isidentifier():
                raise NameError

            self.token_idx += 2
            value = self.tokens[self.token_idx]

            self.vars.append(Variable(name, var_type, value))
            self.token_idx += 1
        else:
            self.get_var_from_ident(self.tokens[self.token_idx]).val = self.tokens[self.token_idx + 2]
            self.token_idx += 3

    def parse(self):
        self.token_idx: int = 0
        while self.token_idx < len(self.tokens):
            if (func_token := self.tokens[self.token_idx]) in self.builtin_functions:
                self.token_idx += 1
                if self.tokens[self.token_idx] != "(":
                    print("Error: Expected `(`")
                    exit(1)

                self.token_idx += 1
                args: list = []

                while self.tokens[self.token_idx] != ")":
                    args.append(self.tokens[self.token_idx])
                    self.token_idx += 1

                try:
                    self.builtin_functions[func_token](args)
                except SyntaxError:
                    print(f"Error: Args passed to `{func_token}` is not right.")
                    exit(1)
            elif func_token == "var":
                try:
                    self.parse_var()
                except NameError:
                    print(f"Error bad identifier name {self.tokens[self.token_idx]}")
                    exit(1)
            elif func_token in self.get_var_names():
                self.parse_var()  # No need to catch exception because we won't allow a bad identifier name
            else:
                if func_token not in Tokeniser.tokens_to_find:
                    print(f"Unknown function or key word `{func_token}`.")
                    exit(1)

            self.token_idx += 1
