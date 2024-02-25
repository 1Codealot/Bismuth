from Tokenisation import Tokeniser



class Variable:
    def __init__(self, ident: str, type_of: str, val: str):
        self.ident = ident
        self.type_of = type_of
        self.val = val


class CodeGenerator:
    # TODO: Stack methods to keep track of stack.

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

        self.included: list[str] = []

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

    def get_var_stack_offset(self, v: Variable):
        return len(self.vars) - self.vars.index(v)

    def write_print(self, args: list[str]):
        if len(args) != 1:
            raise SyntaxError

        if "print" not in self.included:
            self.included.append("print")

        self.data.append(f"""
    s{self.strings} db {str(list(map(ord, args[0].strip('"').encode().decode('unicode_escape')))).strip("[]")}, 0
    s{self.strings}l equ $ - s{self.strings}""")

        self.text.append(
            f"""
    mov rax, s{self.strings}l
    push rax

    mov rax, s{self.strings}
    push rax""")

        self.vars.append(Variable(f"s{self.strings}l", "str", ""))
        self.vars.append(Variable(f"s{self.strings}", "str", ""))

        self.text.append(
            f"""
    call print
    
    pop rax
    pop rax""")
        
        self.vars.pop(len(self.vars) - 1)
        self.vars.pop(len(self.vars) - 1)
        
        self.strings += 1

    def write_exit(self, args: list[str]):
        if len(args) != 1:
            raise SyntaxError

        if "exit" not in self.included:
            self.included.append("exit")

        if args[0] in self.get_var_names():
            var = self.get_var_from_ident(args[0])  # No need to catch error because we check right above

            if var.type_of != "int":
                print(f"Type of variable {var.ident} not `int`")

        else:
            print(f"Error no var called `{args[0]}` doesn't exist")
            exit(1)

        self.text.append(
            f"""
    mov rax, [ rsp + {(self.get_var_stack_offset(var) - 1) * 8} ]
    push rax

    call exit
    
    pop rax""")

    def write_code(self):
        with open("./out/out.asm", 'w') as f:

            for inc in self.included:
                f.write(f'%include "../src/include/builtins/{inc}.asm"\n')

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

            while value in self.get_var_names():
                value = self.get_var_from_ident(value).val

            self.vars.append(Variable(name, var_type, value))

            self.text.append(f"""
    mov rax, {value} ; {name}
    push rax""")

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
