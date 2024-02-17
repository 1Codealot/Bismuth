#!/usr/bin/python3

import sys
import Tokenisation.Tokeniser as Tokeniser


def main():
    if len(sys.argv) < 2:
        print("Usage: Py--.py <file>")
        return
    file = sys.argv[1]

    with open(file, "r") as f:
        code = f.read()

        tokeniser: Tokeniser = Tokeniser.Tokeniser(code)

        print(f"Tokens: {tokeniser.tokenise()}")


if __name__ == "__main__":
    main()
