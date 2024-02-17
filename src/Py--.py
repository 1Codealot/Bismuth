#!/usr/bin/python3

import sys
import Generation.Generate
import time


def main():
    if len(sys.argv) < 2:
        print("Usage: Py--.py <file>")
        return
    file = sys.argv[1]

    code_gen = Generation.Generate.CodeGenerator(file)


if __name__ == "__main__":
    t1 = time.time()
    main()
    print(f"Time taken: {time.time() - t1}")
