#!/usr/bin/python3

import sys
import Generation.Generate
import time
import os


def main():
    if len(sys.argv) < 2:
        print("Usage: Py--.py <file>")
        return
    file = sys.argv[1]

    code_gen = Generation.Generate.CodeGenerator(file)
    code_gen.parse()

    code_gen.write_code()


if __name__ == "__main__":
    t1 = time.time()
    main()
    print(f"Time taken: {time.time() - t1}")
    os.chdir("out")
    nasm = os.system("nasm out.asm -felf64")
    if nasm != 0:
        exit(nasm)

    ld = os.system("ld -o out out.o")
    if ld != 0:
        exit(ld)

    if "run" in sys.argv:
        prog = os.system("./out")
        exit(prog)
